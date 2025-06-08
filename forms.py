from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FloatField, DateField
from wtforms.validators import DataRequired, Email, EqualTo, Length

class RegisterForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=6)])
    confirm = PasswordField("Confirm Password", validators=[DataRequired(), EqualTo("password")])
    submit = SubmitField("Create Account")

class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Log In")

class PaycheckForm(FlaskForm):
    date = DateField("Paycheck Date", validators=[DataRequired()])
    amount = FloatField("Amount", validators=[DataRequired()])
    submit = SubmitField("Add Paycheck")

class BillForm(FlaskForm):
    name = StringField("Bill Name", validators=[DataRequired()])
    date = DateField("Due Date", validators=[DataRequired()])
    amount = FloatField("Amount", validators=[DataRequired()])
    submit = SubmitField("Add Bill")
