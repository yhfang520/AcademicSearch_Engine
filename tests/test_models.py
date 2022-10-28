import warnings
warnings.filterwarnings("ignore")
import os
basedir = os.path.abspath(os.path.dirname(__file__))
import unittest
from app import create_app, db
from app.Model.models import Student, Faculty, User, Positions, Researchfield, Application
from config import Config


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    ROOT_PATH = '..//'+basedir
    
class TestModels(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_password_hashing(self):
        u = User(email='student1@wsu.edu', id='0116',status='student')
        u.set_password('123')
        self.assertFalse(u.get_password('234'))
        self.assertTrue(u.get_password('123'))

    def test_student1_info(self):
        u1 = User(email='student1@wsu.edu', id='0116',status='student')
        db.session.add(u1)
        db.session.commit()
        self.assertEqual(u1.get_user_posts().all(), [])
        p1 = Student(firstname='John', lastname='Yates', culmulative_gpa=3.8, prior_research_exp='TA',phone_number=3656789,user_id=u1.id )
        db.session.add(p1)
        db.session.commit()
        self.assertEqual(u1.get_user_posts().count(), 1)
        self.assertEqual(u1.get_user_posts().first().firstname, 'John')
        self.assertEqual(u1.get_user_posts().first().lastname, 'Yates')
        self.assertEqual(u1.get_user_posts().first().culmulative_gpa, 3.8)
        self.assertEqual(u1.get_user_posts().first().prior_research_exp, 'TA')
        self.assertEqual(u1.get_user_posts().first().phone_number, 3656789)
    
    def test_student2_info(self):
        u1 = User(email='john.yates@wsu.com')
        u2 = User(email='amit.khan@wsu.com')
        db.session.add(u1)
        db.session.add(u2)
        db.session.commit()
        self.assertEqual(u1.get_user_posts().all(), [])
        self.assertEqual(u2.get_user_posts().all(), [])
        p1 = Student(firstname='John1', lastname='Yates1', culmulative_gpa=3.81, prior_research_exp='TA1',phone_number=36567891,user_id=u1.id )
        db.session.add(p1)
        p2 = Student(firstname='Amit', lastname='Khan', culmulative_gpa=3.9, prior_research_exp='TA*2',phone_number=1234567,user_id=u1.id )
        db.session.add(p2)
        db.session.commit()
        p3 = Student(firstname='CptS', lastname='322', culmulative_gpa=4.0, prior_research_exp='TA*3',phone_number=9876543,user_id=u2.id )
        db.session.add(p3)
        db.session.commit()
        # test the posts by the first user
        self.assertEqual(u1.get_user_posts().count(), 2)
        self.assertEqual(u1.get_user_posts().all()[1].firstname, 'Amit')
        self.assertEqual(u1.get_user_posts().all()[1].lastname, 'Khan')
        self.assertEqual(u1.get_user_posts().all()[1].culmulative_gpa, 3.9)
        self.assertEqual(u1.get_user_posts().all()[1].prior_research_exp, 'TA*2')
        self.assertEqual(u1.get_user_posts().all()[1].phone_number, 1234567)
        # test the posts by the second user
        self.assertEqual(u2.get_user_posts().count(), 1)
        self.assertEqual(u2.get_user_posts().all()[0].firstname, 'CptS')
        self.assertEqual(u2.get_user_posts().all()[0].lastname, '322')
        self.assertEqual(u2.get_user_posts().all()[0].culmulative_gpa, 4.0)
        self.assertEqual(u2.get_user_posts().all()[0].prior_research_exp, 'TA*3')
        self.assertEqual(u2.get_user_posts().all()[0].phone_number, 9876543)
    
    def test_faculty1_info(self):
        u3 = User(email='sakire.arslanay@wsu.edu', id='0118')
        db.session.add(u3)
        db.session.commit()
        self.assertEqual(u3.get_user_posts2().all(), [])
        p4 = Faculty(firstname='Sakire', lastname='Arslan', phone_number=5093354089,user_id=u3.id )
        db.session.add(p4)
        db.session.commit()
        self.assertEqual(u3.get_user_posts2().count(),1)
        self.assertEqual(u3.get_user_posts2().all()[0].firstname, 'Sakire')
        self.assertEqual(u3.get_user_posts2().all()[0].lastname, 'Arslan')
        self.assertEqual(u3.get_user_posts2().all()[0].phone_number, 5093354089)

    def test_faculty2_info(self):
        u1 = User(email='faculty1@wsu.com')
        u2 = User(email='faculty2@wsu.com')
        db.session.add(u1)
        db.session.add(u2)
        db.session.commit()
        self.assertEqual(u1.get_user_posts2().all(), [])
        self.assertEqual(u2.get_user_posts2().all(), [])
        p1 = Faculty(firstname='Stuart', lastname='Brown', phone_number=11101200,user_id=u1.id )
        db.session.add(p1)
        p2 = Faculty(firstname='Caden', lastname='Weiner', phone_number=9051035,user_id=u1.id )
        db.session.add(p2)
        db.session.commit()
        p3 = Faculty(firstname='Trevor', lastname='Naze', phone_number=1230130,user_id=u2.id )
        db.session.add(p3)
        db.session.commit()
        # test the posts by the first user
        self.assertEqual(u1.get_user_posts2().count(), 2)
        self.assertEqual(u1.get_user_posts2().all()[1].firstname, 'Caden')
        self.assertEqual(u1.get_user_posts2().all()[1].lastname, 'Weiner')
        self.assertEqual(u1.get_user_posts2().all()[1].phone_number, 9051035)
        # test the posts by the second user
        self.assertEqual(u2.get_user_posts2().count(), 1)
        self.assertEqual(u2.get_user_posts2().all()[0].firstname, 'Trevor')
        self.assertEqual(u2.get_user_posts2().all()[0].lastname, 'Naze')
        self.assertEqual(u2.get_user_posts2().all()[0].phone_number, 1230130)
    
    def test_apply(self):
        p1 = Student(firstname='John', lastname='Yates', culmulative_gpa=3.8, prior_research_exp='TA',phone_number=3656789)
        db.session.add(p1)
        db.session.commit()
        u1 = User( email='john.yates@wsu.com')
        c1 = Positions(title='TA', project_information='Grade students work', start_date=1/30,end_date=3/30,required_time_commitment=5,required_gpa=3.5,max_position=3)
        db.session.add(u1)
        db.session.add(c1)
        db.session.commit()
        self.assertEqual(u1.mypositions, [])
        self.assertEqual(c1.applications, [])

        u1.apply(c1)
        db.session.commit()
        self.assertTrue(u1.is_apply(c1))
        self.assertEqual(len(u1.mystudents), 1)
        self.assertEqual(u1.mystudents[0].theposition.max_position,3)
        self.assertEqual(u1.mystudents[0].theposition.title, 'TA')
        self.assertEqual(len(c1.applications), 1)
        self.assertEqual(c1.applications[0].thestudent.email, 'john.yates@wsu.com')


if __name__ == '__main__':
    unittest.main(verbosity=2)