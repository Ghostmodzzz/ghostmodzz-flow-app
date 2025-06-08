from flask import Blueprint, render_template, redirect, url_for, flash, request
from extensions import db
from forms import RegisterForm, LoginForm, PaycheckForm, BillForm
from models import User, Paycheck, Bill
from flask_login import login_user, login_required, logout_user, current_user
from services.mail import send_confirmation_email
from itsdangerous import URLSafeTimedSerializer
from config import Config
from services.ai import get_budget_recommendation

main = Blueprint("main", __name__)

# Serializer for confirmation tokens
serializer = URLSafeTimedSerializer(Config.SECRET_KEY)

# NEW root route
@main.route("/")
def home():
    return redirect(url_for("main.login"))

@main.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(email=form.email.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()

        token = serializer.dumps(user.email, salt=Config.SECURITY_PASSWORD_SALT)
        send_confirmation_email(user.email, token)

        return redirect(url_for("main.loading"))
    return render_template("register.html", form=form)

@main.route("/confirm/<token>")
def confirm_email(token):
    try:
        email = serializer.loads(
            token,
            salt=Config.SECURITY_PASSWORD_SALT,
            max_age=3600
        )
    except:
        flash("The confirmation link is invalid or has expired.", "danger")
        return redirect(url_for("main.login"))

    user = User.query.filter_by(email=email).first_or_404()
    user.confirmed = True
    db.session.commit()

    flash("Email confirmed. Please log in.", "success")
    return redirect(url_for("main.login"))

@main.route("/loading")
def loading():
    return render_template("loading.html")

@main.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.password == form.password.data and user.confirmed:
            login_user(user)
            return redirect(url_for("main.dashboard"))
        flash("Invalid credentials or email not confirmed.", "danger")
    return render_template("login.html", form=form)

@main.route("/dashboard", methods=["GET", "POST"])
@login_required
def dashboard():
    pform = PaycheckForm(prefix="p")
    bform = BillForm(prefix="b")

    # handle paycheck submissions
    if pform.validate_on_submit() and pform.submit.data:
        db.session.add(
            Paycheck(
                date=pform.date.data,
                amount=pform.amount.data,
                user=current_user
            )
        )
        db.session.commit()

    # handle bill submissions
    if bform.validate_on_submit() and bform.submit.data:
        db.session.add(
            Bill(
                name=bform.name.data,
                date=bform.date.data,
                amount=bform.amount.data,
                user=current_user
            )
        )
        db.session.commit()

    paychecks = Paycheck.query.filter_by(user=current_user).all()
    bills     = Bill.query.filter_by(user=current_user).all()

    # AI-driven budget recommendation
    recommendation = get_budget_recommendation(paychecks, bills)

    return render_template(
        "dashboard.html",
        pform=pform,
        bform=bform,
        paychecks=paychecks,
        bills=bills,
        recommendation=recommendation
    )

@main.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("main.login"))
