from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from flask_login import UserMixin
from app import login
#from app.Controller.routes import position


class Student(UserMixin,db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(150))
    lastname = db.Column(db.String(150))
    email = db.Column(db.String(120), index=True)
    culmulative_gpa = db.Column(db.Integer)
    prior_research_exp = db.Column(db.String(200))
    phone_number = db.Column(db.Integer)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'))
 
class Faculty(UserMixin,db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(150))
    lastname = db.Column(db.String(150))
    email = db.Column(db.String(120), index=True)
    phone_number = db.Column(db.Integer)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'))
    #positions=db.relationship('Positions',secondary = position, primaryjoin=(position.c.faculty_id == id),backref=db.backref('position', lazy='dynamic'),lazy='dynamic')
    def get_position(self):
        return self.positions

class User(UserMixin,db.Model):
    email = db.Column(db.String(120), index=True)
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(150))
    password_hash = db.Column(db.String(128))
    students = db.relationship('Student',backref='writer',lazy='dynamic')
    facultys =db.relationship('Faculty',backref ='writer',lazy='dynamic')
    mypositions =db.relationship('Positions',back_populates ='thefaculty')
    mystudents =db.relationship('Application',back_populates ='thestudent')

    def __repr__(self):
        return '<Id: {} email:{} status:{} >' .format(self.id, self.email,self.status)

    def get_user_posts(self):
        return self.students

    def get_user_posts2(self):
        return self.facultys
            
    def set_password(self, password):
       self.password_hash = generate_password_hash(password)
    
    def get_password(self, password):
       return check_password_hash(self.password_hash, password)

    def apply(self,newstudent):
            newApply = Application(theposition = newstudent)
            self.mystudents.append(newApply)
            db.session.commit()

    def is_apply(self,newstudent):
        return (Application.query.filter_by(student_id=self.id).filter_by(position_id=newstudent.id).count() > 0)

    def withdraw(self,oldstudent):
        if(self.is_apply(oldstudent)):
            curApply = Application.query.filter_by(student_id=self.id).filter_by(position_id=oldstudent.id).first()
            db.session.delete(curApply)
            db.session.commit()

    def enrolled(self):
         return self.mystudents

    



class Positions(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(150))
    lastname = db.Column(db.String(150))
    phone_number = db.Column(db.Integer)
    title = db.Column(db.String(150))
    project_information = db.Column(db.String(200))
    start_date = db.Column(db.String(200)) 
    end_date = db.Column(db.String(200))
    required_time_commitment = db.Column(db.Integer)
    required_gpa = db.Column(db.Integer)
    major = db.Column(db.String(150))
    required_course = db.Column(db.String(200))
    max_position = db.Column(db.Integer)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'))
    thefaculty = db.relationship('User',back_populates ='mypositions')
    applications = db.relationship('Application',back_populates ='theposition')
    def __repr__(self):
        return '<firstname:{} lastname:{} phone number:{} title:{} project_information:{}  start_date:{} end_date:{}  end_date:{} required_time_commitment: {} required_gpa:{} major:{} required_course:{} max_position:{}>' .format(self.id, self.firstname,self.lastname,self.phone_number,self.title,self.project_information,self.start_date,self.end_date,self.required_time_commitment,self.required_gpa,self.major, self.required_course,self.max_position)

class Researchfield(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    field = db.Column(db.String(150))

class Application(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(20), default = "Pending")
    position_id= db.Column(db.Integer,db.ForeignKey('positions.id'))
    student_id= db.Column(db.Integer,db.ForeignKey('user.id'))
    major=db.Column(db.String(150))
    taking_courses=db.Column(db.String(200))
    reason=db.Column(db.String(200))
    expected_graduation=db.Column(db.String(200))
    thestudent = db.relationship('User',back_populates ='mystudents')
    theposition = db.relationship('Positions',back_populates ='applications')

    def __repr__(self):
        return 'Applied Position {} student: {} >'.format(self.thestudent,self.theposition)
 

@login.user_loader
def load_user(id):
    return User.query.get(int(id))
