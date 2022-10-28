from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField,TextAreaField,FloatField,IntegerField,BooleanField
from wtforms.validators import  DataRequired, Length,ValidationError
from wtforms_sqlalchemy.fields import QuerySelectMultipleField
from wtforms.widgets import ListWidget, CheckboxInput
from app.Model.models import Student

class PostForm(FlaskForm):

    firstname = StringField('First Name', validators=[DataRequired()])
    lastname = StringField('Last Name', validators=[DataRequired()])
    phone_number =IntegerField('Phone Number',validators=[DataRequired()])
    culmulative_gpa = FloatField('Cum GPA', validators=[DataRequired()])
    prior_research_exp = TextAreaField('prior research experience', validators=[DataRequired(),Length(min=1,max=1500)])
    submit = SubmitField('Post')


    

class FacultyForm(FlaskForm): 
    firstname = StringField('First Name', validators=[DataRequired()])
    lastname = StringField('Last Name', validators=[DataRequired()])
    phone_number =IntegerField('Phone Number',validators=[DataRequired()])
    submit = SubmitField('Post')

    
class PositionForm(FlaskForm):
    firstname = StringField('First Name', validators=[DataRequired()])
    lastname = StringField('Last Name', validators=[DataRequired()])
    phone_number =IntegerField('Phone Number',validators=[DataRequired()])
    title = StringField('Title', validators=[DataRequired()])
    project_information = TextAreaField('Project Information', validators=[DataRequired(),Length(min=1,max=1500)])
    start_date = StringField('Start Date', validators=[DataRequired()])
    end_date = StringField('End Date', validators=[DataRequired()])
    required_time_commitment = IntegerField('Time Commitment',validators=[DataRequired()])
    required_gpa = FloatField('Required GPA',validators=[DataRequired()])
    required_course =TextAreaField('Required Course', validators=[DataRequired(),Length(min=1,max=1500)])
    major  = SelectField('Majors', choices = [('Math','Math'),('History','History'),('Art','Art'),('Cpts','Cpts'),('EE','EE'),('Engineer','Engineer')])
    max_position = IntegerField('Max Position',validators=[DataRequired()])
    submit = SubmitField('Post')

class EmptyForm(FlaskForm):
    delete = SubmitField('Delete')


class ApplyForm(FlaskForm):
    #status = StringField('Status', validators=[DataRequired()])
    apply = SubmitField('Apply')
    major=StringField('Major / Minor', validators=[DataRequired()])
    taking_courses=StringField('Taking Courses', validators=[DataRequired()])
    reason=StringField('Why are you applying this position?', validators=[DataRequired()])
    expected_graduation=SelectField('Expected Graduation Term', choices=[('2022 Spring','2022 Spring'),('2022 Fall','2022 Fall'),('2023 Spring','2023 Spring'),('2023 Fall','2023 Fall'),('2024 Spring','2024 Spring')])
    submit = SubmitField('Post')

class ViewForm(FlaskForm):
    view = SubmitField('View')

class SortForm(FlaskForm):
    check = BooleanField('Display my major only')
    submit = SubmitField('Refresh')
    majors  = SelectField('Majors', choices = [('Math','Math'),('History','History'),('Art','Art'),('Cpts','Cpts'),('EE','EE'),('Engineer','Engineer')])

