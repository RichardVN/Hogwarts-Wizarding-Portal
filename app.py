from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime
import os

# house to integer
house_to_id = {
    "Gryffindor": 1,
    "Slytherin": 2,
    "Hufflepuff": 3,
    "Ravenclaw": 4
}


# create instance of Flask class, which acts as our Web Server Gateway Interface (WSGI) app
# argument is name of the app's module. We use __name__ because we run as '__main__'
app = Flask(__name__)


def get_env_variable(name):
    try:
        return os.environ[name]
    except KeyError:
        message = "Expected environment variable '{}' not set.".format(name)
        raise Exception(message)


# the values of those depend on your setup
POSTGRES_URL = get_env_variable("POSTGRES_URL")
POSTGRES_USER = get_env_variable("POSTGRES_USER")
POSTGRES_PW = get_env_variable("POSTGRES_PW")
POSTGRES_DB = get_env_variable("POSTGRES_DB")


# Dev environment?
ENV = 'dev'

# Config DB URI of localhost or heroku server
if ENV == 'dev':
    app.debug = True
    DB_URL = 'postgresql+psycopg2://{user}:{pw}@{url}/{db}'.format(
        user=POSTGRES_USER, pw=POSTGRES_PW, url=POSTGRES_URL, db=POSTGRES_DB)
    # app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://user:password@localhost:5432/HWP'
    app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL
else:
    app.debug = False

# Silence deprecation warning
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# create db object
db = SQLAlchemy(app)

# create model for db


class Houses(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    mascot = db.Column(db.String(255), nullable=False)
    founder = db.Column(db.String(255), nullable=False)
    head = db.Column(db.String(255), nullable=False)


class Professors(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(255), nullable=False)
    last_name = db.Column(db.String(255), nullable=False)
    house_id = db.Column(db.Integer, db.ForeignKey('houses.id'))


class Students(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(255), nullable=False)
    last_name = db.Column(db.String(255), nullable=False)
    birthdate = db.Column(db.Date, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    house_id = db.Column(db.Integer, db.ForeignKey('houses.id'))


class Classes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    credit = db.Column(db.String(255), nullable=False)
    professor_id = db.Column(db.Integer, db.ForeignKey('professors.id'))


# Many to Many relationship table
registration_table = db.Table('StudentsClasses', db.Model.metadata,
                              db.Column('student_id', db.Integer,
                                        db.ForeignKey('students.id')),
                              db.Column('class_id', db.Integer,
                                        db.ForeignKey('classes.id'))
                              )

# route decorator tells Flask what URL should trigger our function. Just calling a website with url is a GET request.


@app.route('/')
def hi():              # function given a name, which is used to generate URLs for that function (url_for(hi))
    # return ("string")  OR render_template("page.html"), belonging in templates folder
    return render_template('base.html')


@app.route('/index', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        names = ['alice', 'iris', 'katie']
        # pass context from controller app to template html page KWARG
        return render_template('index.html', names=names)
    elif request.method == 'POST':
        # dictionary object contains key-value pairs of "name", "value" attributes from html input element
        data_dictionary = request.form
        fname = request.form.get('first_name')
        names = ['alice', 'iris', 'katie']
        return render_template('index.html', names=names, data=data_dictionary, fname=fname)


@app.route('/students', methods=['POST', 'GET'])
def show_students():
    if request.method == "GET":
        students = Students.query.order_by(Students.last_name).all()
        houses = Houses.query.order_by(Houses.name).all()

        # for each student, get the name of their house from the house id
        student_houses = [Houses.query.filter_by(
            id=student.house_id).first() for student in students]
        for idx, house in enumerate(student_houses):
            student_houses[idx] = house.name

        return render_template('students.html', students=students, houses=houses, student_houses=student_houses)
    elif request.method == 'POST':
        if request.form['post_type'] == "add":
            print("\n------- index POST add -----")
            print("Adding a student to the database")

            first_name = request.form['first_name']
            last_name = request.form['last_name']
            birthdate = request.form['birthdate']
            year = request.form['year']
            house_id = request.form['house_id']

            new_student = Students(
                first_name=first_name, last_name=last_name, birthdate=birthdate, year=year, house_id=house_id)
            print('POST: new student entry successfully added')
            db.session.add(new_student)
            db.session.commit()
            return redirect('/students')

        # delete 'post_type' == 'delete'
        else:
            print("\n------- index POST delete -----")
            print("deleting a student to the database")
            delete_id = request.form['delete_id']
            student_to_delete = Students.query.filter_by(id=delete_id).first()
            print(
                f"Deleting ID:{student_to_delete.id}, {student_to_delete.first_name} {student_to_delete.last_name}")
            db.session.delete(student_to_delete)
            db.session.commit()

            return redirect('/students')


@app.route('/houses', methods=['POST', 'GET'])
def show_houses():
    return render_template('houses.html')


@app.route('/professors', methods=['POST', 'GET'])
def show_professors():
    return render_template('professors.html')


@app.route('/classes', methods=['POST', 'GET'])
def show_classes():
    return render_template('classes.html')


@app.route('/registrations', methods=['POST', 'GET'])
def show_registrations():
    return render_template('registrations.html')
