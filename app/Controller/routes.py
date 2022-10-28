from __future__ import print_function
import functools
import sys
from flask import Blueprint
from flask import render_template, flash, redirect, url_for, request
from config import Config
from flask_login import current_user, login_required
from app import db
from app.Model.models import Student,Faculty,Positions,User,Application
from app.Controller.forms import PostForm,FacultyForm,PositionForm,EmptyForm,ApplyForm,ViewForm,SortForm
from functools import wraps

bp_routes = Blueprint('routes', __name__)
bp_routes.template_folder = Config.TEMPLATE_FOLDER #'..\\View\\templates'


@bp_routes.route('/', methods=['GET','POST'])
@bp_routes.route('/Student/', methods=['GET','POST'])
@login_required
def index():
    applicationform=ApplyForm()
    if(current_user.status=="student"):
        #print(current_user.enrolled())
        return render_template('Student.html',title="Display profile",student=Student.query.filter_by(user_id=current_user.id).all(),apply=current_user.enrolled())
    else:
       return render_template('404error.html')
    
  
@bp_routes.route('/Faculty', methods=['GET','POST'])
@login_required
def index2():
  emptyform = EmptyForm()
  if(current_user.status=="faculty"):
    return render_template('Faculty.html',title="Display profile",faculty=Faculty.query.filter_by(user_id=current_user.id).all(),position=current_user.mypositions,eform=EmptyForm())
  else:
    return render_template('404error.html')


@bp_routes.route('/editStudent/', methods=['GET' , 'POST'])
@login_required
def create():
    cform = PostForm()
    if(current_user.status=="student"):
            studentt = Student.query.filter_by(user_id=current_user.id).first()
            if request.method =='GET':
             cform.firstname.data = studentt.firstname
             cform.lastname.data = studentt.lastname
             cform.phone_number.data =studentt.phone_number
             cform.culmulative_gpa.data=studentt.culmulative_gpa
             cform.prior_research_exp.data = studentt.prior_research_exp
            elif request.method=='POST':
             studentt.firstname = cform.firstname.data
             studentt.lastname = cform.lastname.data
             studentt.phone_number = cform.phone_number.data
             studentt.culmulative_gpa=cform.culmulative_gpa.data
             studentt.prior_research_exp = cform.prior_research_exp.data
             db.session.commit()
             flash("Your Profile is Created")
             return redirect(url_for('routes.index'))
            else:
                pass
            return render_template('create.html',form = cform)
    else:
      return render_template('404error.html')


@bp_routes.route('/editFaculty', methods=['GET' , 'POST'])
@login_required
def create2():
    pform = FacultyForm()
    if(current_user.status=="faculty"):
            facultyy = Faculty.query.filter_by(user_id=current_user.id).first()
            if request.method =='GET':
       #post = Faculty(user_id = current_user.id,firstname=pform.firstname.data,lastname=pform.lastname.data,email=current_user.email,phone_number=pform.phone_number.data)
                 pform.firstname.data = facultyy.firstname
                 pform.lastname.data = facultyy.lastname
                 pform.phone_number.data =facultyy.phone_number
            elif request.method=='POST':
                 facultyy.firstname = pform.firstname.data
                 facultyy.lastname = pform.lastname.data
                 facultyy.phone_number = pform.phone_number.data
                 db.session.commit()
                 flash("Your Profile is Created")
                 return redirect(url_for('routes.index2'))
            else:
                pass
            return render_template('create2.html',form = pform)
    else:
        return render_template('404error.html')


@bp_routes.route('/createPositions/', methods=['GET' , 'POST'])
@login_required
def position():
    rform = PositionForm()
    if(current_user.status=="faculty"):
      if rform.validate_on_submit():
          post3 = Positions(user_id=current_user.id,firstname=rform.firstname.data,lastname=rform.lastname.data,phone_number=rform.phone_number.data,title = rform.title.data,project_information=rform.project_information.data,start_date=rform.start_date.data,end_date=rform.end_date.data,required_time_commitment=rform.required_time_commitment.data,required_gpa = rform.required_gpa.data,major = rform.major.data, required_course=rform.required_course.data,max_position=rform.max_position.data)
          db.session.add(post3)
          db.session.commit()
          flash("Research Positions is Created")
          return redirect(url_for('routes.index2'))
      return render_template('Positions.html',form = rform)
    else:
      return render_template('404error.html')

@bp_routes.route('/viewPositions/', methods=['GET'])
@login_required
def display_profile():
    aform = ApplyForm()
    if(current_user.status=="student"):
        return render_template('vpost.html',title="Display position",position=Positions.query.all(),aform=ApplyForm())
    else:
       return render_template('404error.html')
   

@bp_routes.route('/delete/<user_id>', methods =['DELETE','POST'])
@login_required
def delete(user_id):
  if(current_user.status=="faculty"):
    post = Positions.query.filter_by(user_id=current_user.id).first()
    db.session.delete(post)
    db.session.commit()
    flash("Delete Successfully")
    return redirect(url_for('routes.index2'))
  else:
    return render_template('404error.html')
 

@bp_routes.route('/applyPositions/<positions_id>', methods=['POST'])
@login_required
def apply_profile(positions_id):
  applicationform = ApplyForm()
  if(current_user.status=="student"):
        if applicationform.validate_on_submit():
            #theposition=Positions.query.filter_by(id=positions_id).first()
            #current_user.apply(theposition)
            post3 = Application(position_id=positions_id,student_id=current_user.id,major=applicationform.major.data,taking_courses=applicationform.taking_courses.data,reason=applicationform.reason.data, expected_graduation=applicationform.expected_graduation.data)
            db.session.add(post3)
            db.session.commit()
            flash("Apply Successfully")
            return redirect(url_for('routes.index'))
        return render_template('Qualification.html',form=applicationform)
  else:
       return render_template('404error.html')

# position_id = positions_id

#@bp_routes.route('/qualification/', methods=['GET','POST'])
#@login_required
#def qualification():
#    aform = ApplyForm()
#    if(current_user.status=="student"):
#        return render_template('Qualification.html',title="Apply",aform=ApplyForm())
#    else:
#       return render_template('404error.html')





@bp_routes.route('/viewStudent/', methods=['GET','POST'])
@login_required
def view_profile():
    vform = ViewForm()
    if(current_user.status=="faculty"):
        return render_template('vpost.html',title="Display position",position=current_user.mypositions,vform=ViewForm())
    else:
       return render_template('404error.html')


@bp_routes.route('/applicationStatus/', methods=['GET'])
@login_required
def view_application():
    aform = ApplyForm()
    if(current_user.status=="student"):
        return render_template('view_application.html',title="Application Status",position=Positions.query.all(),aform=ApplyForm())
    else:
       return render_template('404error.html')


@bp_routes.route('/viewapplicant/<positions_id>', methods=['GET','POST'])
@login_required
def view_applicant(positions_id):
    if(current_user.status=="faculty"):
        return render_template('view_applicant.html',title="View Applicant",apply=Application.query.filter_by(position_id=positions_id).all())
    else:
       return render_template('404error.html')

@bp_routes.route('/acceptApplicant/<id>', methods=['POST'])
@login_required
def accept_applicant(id):
  if(current_user.status=="faculty"):
    apply=Application.query.filter_by(id=id).first()
    #return render_template('new.html',title="View Applicant",apply=Application.query.all())
    apply.status = "Approved"
    db.session.commit()
    flash("Upload Successfully")
    return redirect(url_for('routes.index2'))
  else:
    return render_template('404error.html')


@bp_routes.route('/interviewApplicant/<id>', methods=['POST'])
@login_required
def interview_applicant(id):
  if(current_user.status=="faculty"):
    apply=Application.query.filter_by(id=id).first()
    #return render_template('new.html',title="View Applicant",apply=Application.query.all())
    apply.status = "Interview"
    db.session.commit()
    flash("Upload Successfully")
    return redirect(url_for('routes.index2'))
  else:
    return render_template('404error.html')

@bp_routes.route('/delayApplicant/<id>', methods=['POST'])
@login_required
def delay_applicant(id):
  if(current_user.status=="faculty"):
    apply=Application.query.filter_by(id=id).first()
    #return render_template('new.html',title="View Applicant",apply=Application.query.all())
    apply.status = "Not Approved"
    db.session.commit()
    flash("Upload Successfully")
    return redirect(url_for('routes.index2'))
  else:
    return render_template('404error.html')


@bp_routes.route('/withdrawPositions/<positions_id>', methods=['POST'])
@login_required
def withdraw(positions_id):
    if(current_user.status=="student"):
      theposition=Positions.query.filter_by(id=positions_id).first()
      current_user.withdraw(theposition)
      db.session.commit()
      flash("Withdraw Successfully")
      return redirect(url_for('routes.index'))
    else:
      return render_template('404error.html')


@bp_routes.route('/major/', methods=['GET' , 'POST'])
@login_required
def majors():
    sort_form = SortForm()
    if(current_user.status=="student"):
        return render_template('major.html',title="Display position", majorasd = Positions.query.filter_by(major="Math").all(),form = sort_form)
    else:
        return render_template('404error.html')

  
