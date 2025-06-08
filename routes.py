from flask import Blueprint, render_template, redirect, url_for, flash, request
from extensions import db, login_manager
from models import User, BankAccount, Transaction, Bill, Paycheck
from forms import RegistrationForm, LoginForm, BillForm, PaycheckForm
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from services.plaid_service import exchange_public_token, get_accounts, get_transactions
from datetime import date, timedelta

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return redirect(url_for('main.dashboard'))

@main.route('/register', methods=['GET','POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data,
                    password=generate_password_hash(form.password.data))
        db.session.add(user)
        db.session.commit()
        flash('Account created! Please log in.', 'success')
        return redirect(url_for('main.login'))
    return render_template('register.html', form=form)

@main.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        u = User.query.filter_by(email=form.email.data).first()
        if u and check_password_hash(u.password, form.password.data):
            login_user(u)
            return redirect(url_for('main.dashboard'))
        flash('Invalid credentials', 'danger')
    return render_template('login.html', form=form)

@main.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.login'))

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

@main.route('/dashboard', methods=['GET','POST'])
@login_required
def dashboard():
    bill_form = BillForm(prefix='bill')
    pc_form   = PaycheckForm(prefix='pc')

    # handle manual paycheck
    if pc_form.validate_on_submit():
        pc = Paycheck(date=pc_form.date.data,
                      amount=pc_form.amount.data,
                      is_manual=True,
                      user_id=current_user.id)
        db.session.add(pc)
        db.session.commit()
        flash('Paycheck added!', 'success')
        return redirect(url_for('main.dashboard'))

    # handle new bill
    if bill_form.validate_on_submit():
        b = Bill(name=bill_form.name.data,
                 amount=bill_form.amount.data,
                 due_date=bill_form.due_date.data,
                 user_id=current_user.id)
        db.session.add(b)
        db.session.commit()
        flash('Bill added!', 'success')
        return redirect(url_for('main.dashboard'))

    # gather data for display
    bills    = Bill.query.filter_by(user_id=current_user.id).order_by(Bill.due_date).all()
    paychecks= _calculate_paychecks(current_user)

    return render_template('dashboard.html',
                           bills=bills,
                           paychecks=paychecks,
                           bill_form=bill_form,
                           pc_form=pc_form)

def _calculate_paychecks(user):
    # manual entries
    rows = []
    for pc in Paycheck.query.filter_by(user_id=user.id).order_by(Paycheck.date):
        rows.append({
            'date': pc.date,
            'amount': float(pc.amount),
            'allocations': _allocations(float(pc.amount), user)
        })

    # auto-detect via Plaid
    today = date.today()
    start = today - timedelta(days=14)
    for acct in user.bank_accounts:
        txns = get_transactions(acct.plaid_access_token, start.isoformat(), today.isoformat())
        for t in txns:
            if t['amount'] >= 1000:
                rows.append({
                    'date': t['date'],
                    'amount': t['amount'],
                    'allocations': _allocations(t['amount'], user)
                })
    return rows

def _allocations(amount, user):
    rem = amount
    allocs = []
    for b in Bill.query.filter_by(user_id=user.id).order_by(Bill.due_date):
        take = min(rem, float(b.amount))
        allocs.append({'bill': b.name, 'allocated': take})
        rem -= take
    return allocs

@main.route('/link_bank', methods=['POST'])
@login_required
def link_bank():
    public_token = request.form['public_token']
    at = exchange_public_token(public_token)
    for acct in get_accounts(at):
        db.session.add(BankAccount(
            plaid_access_token=at,
            account_id=acct['account_id'],
            institution_name=acct.get('name'),
            user_id=current_user.id))
    db.session.commit()
    flash('Bank linked!', 'success')
    return redirect(url_for('main.dashboard'))
