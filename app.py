# Project: ghostmodzz-flow-app
# Updated files to add authentication, bank linking via Plaid, dashboard, and bill planning.

# app.py
from flask import Flask
from config import Config
from extensions import db, login_manager
from routes import main as main_blueprint
from flask_migrate import Migrate

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)
    Migrate(app, db)

    app.register_blueprint(main_blueprint)
    return app

# expose a global app for Gunicorn
app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
    app = create_app()
    app.run(debug=True)


# config.py
import os

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev")
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL", "sqlite:///dev.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    PLAID_CLIENT_ID = os.environ.get("PLAID_CLIENT_ID")
    PLAID_SECRET = os.environ.get("PLAID_SECRET")
    PLAID_ENV = os.environ.get("PLAID_ENV", "sandbox")


# extensions.py
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = "main.login"


# models.py
from extensions import db
from flask_login import UserMixin
from datetime import date

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    bank_accounts = db.relationship('BankAccount', backref='user')
    bills = db.relationship('Bill', backref='user')

class BankAccount(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    plaid_access_token = db.Column(db.String(255), nullable=False)
    account_id = db.Column(db.String(255), nullable=False)
    institution_name = db.Column(db.String(255))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    account_id = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(255))
    amount = db.Column(db.Numeric(10,2))
    date = db.Column(db.Date)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class Bill(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    amount = db.Column(db.Numeric(10,2))
    due_date = db.Column(db.Date)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


# forms.py
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, DecimalField, DateField
from wtforms.validators import DataRequired, Email, Length, EqualTo

class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In')

class BillForm(FlaskForm):
    name = StringField('Bill Name', validators=[DataRequired()])
    amount = DecimalField('Amount', validators=[DataRequired()])
    due_date = DateField('Due Date', validators=[DataRequired()])
    submit = SubmitField('Add Bill')


# services/plaid_service.py
from plaid import Client
from config import Config

client = Client(
    client_id=Config.PLAID_CLIENT_ID,
    secret=Config.PLAID_SECRET,
    environment=Config.PLAID_ENV
)

def exchange_public_token(public_token):
    res = client.Item.public_token.exchange(public_token)
    return res['access_token']

def get_accounts(access_token):
    return client.Accounts.get(access_token)['accounts']

def get_transactions(access_token, start_date, end_date):
    return client.Transactions.get(access_token, start_date, end_date)['transactions']


# routes.py
from flask import Blueprint, render_template, redirect, url_for, flash, request
from extensions import db, login_manager
from models import User, BankAccount, Transaction, Bill
from forms import RegistrationForm, LoginForm, BillForm
from flask_login import login_user, logout_user, login_required, current_user
from services.plaid_service import exchange_public_token, get_accounts, get_transactions
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import date, timedelta

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return redirect(url_for('main.dashboard'))

@main.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed = generate_password_hash(form.password.data)
        user = User(email=form.email.data, password=hashed)
        db.session.add(user)
        db.session.commit()
        flash('Account created! Please log in.', 'success')
        return redirect(url_for('main.login'))
    return render_template('register.html', form=form)

@main.route('/login', methods=['GET','POST'])
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

@main.route('/dashboard')
@login_required
def dashboard():
    bills = Bill.query.filter_by(user_id=current_user.id).order_by(Bill.due_date).all()
    paychecks = calculate_paychecks(current_user)
    return render_template('dashboard.html', bills=bills, paychecks=paychecks)


def calculate_paychecks(user):
    today = date.today()
    start = today - timedelta(days=14)
    txns = []
    for acct in user.bank_accounts:
        txns += get_transactions(acct.plaid_access_token, start.isoformat(), today.isoformat())
    paychecks = [t for t in txns if t['amount'] > 1000]
    for p in paychecks:
        remaining = p['amount']
        allocations = []
        for bill in Bill.query.filter_by(user_id=user.id).order_by(Bill.due_date):
            amt = min(remaining, float(bill.amount))
            allocations.append({'bill': bill.name, 'allocated': amt})
            remaining -= amt
        p['allocations'] = allocations
    return paychecks

@main.route('/add_bill', methods=['GET','POST'])
@login_required
def add_bill():
    form = BillForm()
    if form.validate_on_submit():
        bill = Bill(name=form.name.data, amount=form.amount.data, due_date=form.due_date.data, user_id=current_user.id)
        db.session.add(bill)
        db.session.commit()
        flash('Bill added!', 'success')
        return redirect(url_for('main.dashboard'))
    return render_template('add_bill.html', form=form)

@main.route('/link_bank', methods=['POST'])
@login_required
def link_bank():
    public_token = request.form.get('public_token')
    access_token = exchange_public_token(public_token)
    accounts = get_accounts(access_token)
    for acct in accounts:
        ba = BankAccount(
            plaid_access_token=access_token,
            account_id=acct['account_id'],
            institution_name=acct.get('name'),
            user_id=current_user.id
        )
        db.session.add(ba)
    db.session.commit()
    flash('Bank linked!', 'success')
    return redirect(url_for('main.dashboard'))


# requirements.txt
Flask
Flask_SQLAlchemy
Flask_Login
Flask_WTF
plaid-python
werkzeug
psycopg2-binary
Flask-Migrate

# Procfile
web: gunicorn app:create_app()
