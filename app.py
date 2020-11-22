from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime
import os

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
migrate = Migrate(app, db)

# create model for db


class Students(db.Model):
    __tablename__ = 'students'
    id = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(255), nullable=False)
    lname = db.Column(db.String(255), nullable=False)
    birthdate = db.Column(db.Date(), nullable=False)
    # house _ ID

    def __init__(self, fname, lname, birthdate):
        self.fname = fname
        self.lname = lname
        self.birthdate = birthdate

    def __repr(self):
        return f'{self.id} {self.fname} {self.lname}'

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
        return render_template('students.html')
    elif request.method == 'POST':
        if request.form['post_type'] == "add":
            print("\n------- index POST add -----")
            print("\nAdding a student to the database")

            # Gather input fields into variables
            first_name = request.form['first_name']
            last_name = request.form['last_name']
            birthdate = request.form['birthdate']
            year = request.form['year']
            house = request.form['house']
        else:
            print('-- delete student POST')


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
