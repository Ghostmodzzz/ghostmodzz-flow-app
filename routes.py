from flask import Blueprint, render_template, redirect, url_for, flash, request
from extensions import db, login_manager
from flask_login import login_user, logout_user, login_required, current_user
from models import User, Bill, Paycheck
from forms import RegisterForm, LoginForm, BillForm, PaycheckForm
from werkzeug.security import generate_password_hash, check_password_hash

main = Blueprint('main', __name__)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='sha256')
        new_user = User(email=form.email.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash('Registration successful. Check your email.', 'success')
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
        else:
            flash('Invalid email or password', 'danger')
    return render_template('login.html', form=form)

@main.route('/dashboard')
@login_required
def dashboard():
    bills = Bill.query.filter_by(user_id=current_user.id).all()
    paychecks = Paycheck.query.filter_by(user_id=current_user.id).all()
    return render_template('dashboard.html', bills=bills, paychecks=paychecks)

@main.route('/add_bill', methods=['GET', 'POST'])
@login_required
def add_bill():
    form = BillForm()
    if form.validate_on_submit():
        bill = Bill(name=form.name.data, amount=form.amount.data, due_date=form.due_date.data, user_id=current_user.id)
        db.session.add(bill)
        db.session.commit()
        flash('Bill added successfully!', 'success')
        return redirect(url_for('main.dashboard'))
    return render_template('add_bill.html', form=form)

@main.route('/add_paycheck', methods=['GET', 'POST'])
@login_required
def add_paycheck():
    form = PaycheckForm()
    if form.validate_on_submit():
        paycheck = Paycheck(amount=form.amount.data, user_id=current_user.id)
        db.session.add(paycheck)
        db.session.commit()
        flash('Paycheck added successfully!', 'success')
        return redirect(url_for('main.dashboard'))
    return render_template('add_paycheck.html', form=form)

@main.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))
