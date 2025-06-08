from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FloatField
from wtforms.validators import DataRequired, Email, Length

class RegisterForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class BillForm(FlaskForm):
    name = StringField('Bill Name', validators=[DataRequired()])
    amount = FloatField('Amount', validators=[DataRequired()])
    due_date = StringField('Due Date', validators=[DataRequired()])
    submit = SubmitField('Add Bill')

class PaycheckForm(FlaskForm):
    amount = FloatField('Paycheck Amount', validators=[DataRequired()])
    submit = SubmitField('Add Paycheck')
