from __future__ import print_function
import sys
from flask import Blueprint
from flask import render_template, flash, redirect, url_for
from flask_sqlalchemy import sqlalchemy
from config import Config
from app import db
from app.Model.models import User,Student,Faculty
from app.Controller.auth_forms import RegistrationForm,LoginForm
from flask_login import current_user, login_user, logout_user, login_required
from app.Controller.forms import PostForm,FacultyForm
bp_auth = Blueprint('auth', __name__)
bp_auth.template_folder = Config.TEMPLATE_FOLDER 

@bp_auth.route('/register',methods=['GET','POST'])
def register():
    sform = RegistrationForm()
    if sform.validate_on_submit():
        userr = User(email=sform.email.data,id=sform.id.data,status=sform.status.data)
        userr.set_password(sform.password.data)
        db.session.add(userr)
        db.session.commit()
        if sform.status.data=='student':
            student = Student(user_id=userr.id)
            db.session.add(student)
            db.session.commit()
        elif sform.status.data =='faculty':
            faculty = Faculty(user_id=userr.id)
            db.session.add(faculty)
            db.session.commit()
         
        flash('Register successfully')
        return redirect(url_for('auth.login'))
    return render_template('Register.html',title='Register',form =sform)

@bp_auth.route('/login/', methods=['GET','POST'])
def login():
    lform = LoginForm()
    if lform.validate_on_submit():
        user = User.query.filter_by(email =lform.email.data).first()
        if(user is None) or (user.get_password(lform.password.data) == False):
            flash('Invalid email')
            return redirect(url_for('auth.login'))
        login_user(user, remember = lform.remember_me.data)
        if (current_user.status =="student"):
          return redirect(url_for('routes.index'))
        else:
          return redirect(url_for('routes.index2'))
    return render_template('login.html',title='Sign In',form = lform)


@bp_auth.route('/logout/', methods=['GET'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login')) 