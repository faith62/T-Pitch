from flask import render_template,redirect,url_for, flash, request
from flask_login import login_user,logout_user, login_required
from . import auth
from ..models import User
from .forms import LoginForm, RegistrationForm
from .. import db
from ..email import mail_message

@auth.route('/login',methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()
        if user is not None and user.check_password(form.password.data):
            login_user(user,form.remember.data)
            return redirect(request.arg.get('next') or url_for('main.index'))

        flash('Invalid username or Password')

    title = "pitch login"
    return render_template('auth/login.html',form = form,title=title)
@auth.route('/register',methods = ["GET","POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email = form.email.data, username = form.username.data,password = form.password.data)
        db.session.add(user)
        db.session.commit()

        # mail_message("Welcome to pitch","email/welcome_user",user.email,user=user)
        
        return redirect(url_for('auth.login'))
        title = "New Account"
    return render_template('auth/register.html',registration_form = form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for("main.index"))
