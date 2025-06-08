from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from extensions import db, login_manager
from models import User, Bill, Paycheck
from forms import RegistrationForm, LoginForm, BillForm, PaycheckForm
from datetime import date

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return redirect(url_for('main.dashboard'))

@main.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(
            email=form.email.data,
            password=generate_password_hash(form.password.data)
        )
        db.session.add(user)
        db.session.commit()
        flash('Account created! Please log in.', 'success')
        return redirect(url_for('main.login'))
    return render_template('register.html', form=form)

@main.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for('main.dashboard'))
        flash('Invalid credentials', 'danger')
    return render_template('login.html', form=form)

@main.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.login'))

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@main.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    bill_form = BillForm(prefix='bill')
    pc_form   = PaycheckForm(prefix='pc')

    # Handle manual paycheck form
    if pc_form.validate_on_submit():
        pc = Paycheck(
            date=pc_form.date.data,
            amount=pc_form.amount.data,
            user_id=current_user.id
        )
        db.session.add(pc)
        db.session.commit()
        flash('Paycheck added!', 'success')
        return redirect(url_for('main.dashboard'))

    # Handle new bill form
    if bill_form.validate_on_submit():
        bill = Bill(
            name=bill_form.name.data,
            amount=bill_form.amount.data,
            due_date=bill_form.due_date.data,
            user_id=current_user.id
        )
        db.session.add(bill)
        db.session.commit()
        flash('Bill added!', 'success')
        return redirect(url_for('main.dashboard'))

    # Query data
    bills = Bill.query.filter_by(user_id=current_user.id).order_by(Bill.due_date).all()
    pcs   = Paycheck.query.filter_by(user_id=current_user.id).order_by(Paycheck.date).all()

    # Calculate allocations
    paychecks = []
    for pc in pcs:
        rem = float(pc.amount)
        allocs = []
        for b in bills:
            take = min(rem, float(b.amount))
            allocs.append({'bill': b.name, 'allocated': take})
            rem -= take
        paychecks.append({
            'date': pc.date,
            'amount': float(pc.amount),
            'allocations': allocs
        })

    return render_template(
        'dashboard.html',
        bills=bills,
        paychecks=paychecks,
        bill_form=bill_form,
        pc_form=pc_form
    )
