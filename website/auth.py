from flask import Blueprint,render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user
from flask_migrate import Migrate


auth = Blueprint('auth', __name__)



@auth.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for("views.home"))
            else:
                flash('Email or password is incorrect', category='error')
                

        else:
            flash('Email or password is incorrect', category='error')

    return render_template('login.html', user=current_user)

@auth.route('/logout')

@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/signup', methods=['GET','POST'])
def sign_up():
    if request.method == 'POST':
      email = request.form.get('email')
      first_name = request.form.get('firstName')  
      password1 = request.form.get('password1')  
      password2 = request.form.get('password2')

      user = User.query.filter_by(email=email).first()
      if user:
          flash('Email already exists', category='error')
      elif len(email) < 4:
          flash('Email must be more than 4 characters.', category='error')
          pass
      elif len(first_name) < 2:
          flash('First name must be more than 2 characters.', category='error')
          pass 
      elif password1 != password2:
          flash('Passwords must be the same.', category='error')
          pass
      elif len(password1) < 7:
          flash('Password must be more than 7 characters.', category='error')
          pass
      else:
          new_user = User(email=email, first_name=first_name, password=generate_password_hash(password1, method='pbkdf2:sha256'))
          db.session.add(new_user)
          db.session.commit()
          flash('Account created successfully!', category='success')
          login_user(new_user, remember=True)
          return redirect(url_for("views.home"))

          pass
    return render_template('sign_up.html', user=current_user)
