from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField,PasswordField,BooleanField,IntegerField, SelectField
from wtforms.validators import  ValidationError, DataRequired, EqualTo, Length,Email
from app.Model.models import User


class RegistrationForm(FlaskForm):
    email = StringField('Email',validators=[DataRequired()])
    password = PasswordField('Password',validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    id = IntegerField('WSU ID',validators=[DataRequired()])
    status = SelectField('Status',choices =[('faculty','faculty'),('student','student')])
    submit = SubmitField('Register')

    
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('The email has already been taken.')    
    
    def validate_id(self, id):
        user = User.query.filter_by(id=id.data).first()
        if user:
            raise ValidationError('The ID  has already been taken.')   


class LoginForm(FlaskForm):
    
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password',validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')