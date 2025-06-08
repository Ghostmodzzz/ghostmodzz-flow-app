from extensions import db
from flask_login import UserMixin

class User(UserMixin, db.Model):
    id            = db.Column(db.Integer, primary_key=True)
    email         = db.Column(db.String(255), unique=True, nullable=False)
    password      = db.Column(db.String(255), nullable=False)
    bank_accounts = db.relationship('BankAccount', backref='user', lazy=True)
    bills         = db.relationship('Bill', backref='user', lazy=True)
    paychecks     = db.relationship('Paycheck', backref='user', lazy=True)

class BankAccount(db.Model):
    id                 = db.Column(db.Integer, primary_key=True)
    plaid_access_token = db.Column(db.String(255), nullable=False)
    account_id         = db.Column(db.String(255), nullable=False)
    institution_name   = db.Column(db.String(255))
    user_id            = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

class Transaction(db.Model):
    id         = db.Column(db.Integer, primary_key=True)
    account_id = db.Column(db.String(255), nullable=False)
    name       = db.Column(db.String(255))
    amount     = db.Column(db.Numeric(10,2))
    date       = db.Column(db.Date)
    user_id    = db.Column(db.Integer, db.ForeignKey('user.id'))

class Bill(db.Model):
    id        = db.Column(db.Integer, primary_key=True)
    name      = db.Column(db.String(255), nullable=False)
    amount    = db.Column(db.Numeric(10,2), nullable=False)
    due_date  = db.Column(db.Date, nullable=False)
    user_id   = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

class Paycheck(db.Model):
    id         = db.Column(db.Integer, primary_key=True)
    date       = db.Column(db.Date, nullable=False)
    amount     = db.Column(db.Numeric(10,2), nullable=False)
    is_manual  = db.Column(db.Boolean, default=True)
    user_id    = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
