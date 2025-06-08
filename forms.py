from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, DecimalField, DateField
from wtforms.validators import DataRequired, Email, Length, EqualTo

class RegistrationForm(FlaskForm):
    email    = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm  = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit   = SubmitField('Create Account')

class LoginForm(FlaskForm):
    email    = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit   = SubmitField('Log In')

class BillForm(FlaskForm):
    name     = StringField('Bill Name', validators=[DataRequired()])
    amount   = DecimalField('Amount', validators=[DataRequired()])
    due_date = DateField('Due Date', validators=[DataRequired()])
    submit   = SubmitField('Add Bill')

class PaycheckForm(FlaskForm):
    date   = DateField('Paycheck Date', validators=[DataRequired()])
    amount = DecimalField('Amount', validators=[DataRequired()])
    submit = SubmitField('Add Paycheck')
