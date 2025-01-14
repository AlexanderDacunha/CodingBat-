from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user


auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if len(request.form) == 2:
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()
        if user:
            if check_password_hash(user.password, password):
                print(f'Logged in {user} successfully')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                print('Incorrect password, try again')
        else:
            print('Username does not exist')

        print("this is a login request")

    else:
        email = request.form.get('email')
        username = request.form.get('username')
        password = request.form.get('password1')
        confirmPassword = request.form.get('password2')

        user = User.query.filter_by(email=email).first()

        if user:
            print("email is already in use")

        elif (email is None) or len(email) < 4:
            flash('Email must be longer than 3 characters.', category='error')

        elif password != confirmPassword:
            flash('Passwords Must Match', category='error')
        
        else:
            new_user = User(email=email, username=username, password=generate_password_hash(password, method='pbkdf2:sha256'))
            db.session.add(new_user)
            db.session.commit()

            login_user(user, remember=True)

            flash("Account created!", category='success')
            print('Account Created and Added!')
            return redirect(url_for('views.home'))

        print("This is a sign up attempt")
    return render_template('login.html', user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

