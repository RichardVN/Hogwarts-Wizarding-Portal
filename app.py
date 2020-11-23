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


# retrieve from environment variables
POSTGRES_URL = get_env_variable("POSTGRES_URL")
POSTGRES_USER = get_env_variable("POSTGRES_USER")
POSTGRES_PW = get_env_variable("POSTGRES_PW")
POSTGRES_DB = get_env_variable("POSTGRES_DB")

# Dev environment?
ENV = 'production'

# Config DB URI of localhost or heroku server
if ENV == 'dev':
    app.debug = True
    DB_URL = 'postgresql+psycopg2://{user}:{pw}@{url}/{db}'.format(
        user=POSTGRES_USER, pw=POSTGRES_PW, url=POSTGRES_URL, db=POSTGRES_DB)
    # ex. app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://user:password@localhost:5432/HWP'
    app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL
else:
    app.debug = False
    app.config['SQLALCHEMY_DATABASE_URI'] = "postgres://izpsqomnrdpxkn:9377d82c606fc291325acd6e23cbdc933079387a4073acb01369f7a7b93b57c1@ec2-52-5-176-53.compute-1.amazonaws.com:5432/d59lmrdv4dc89i"

# Silence deprecation warning
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# create db object
db = SQLAlchemy(app)


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
    house_id = db.Column(db.Integer, db.ForeignKey(
        'houses.id', ondelete='SET NULL'))


# Many to Many relationship table
registration_table = db.Table('StudentsClasses', db.Model.metadata,
                              db.Column('student_id', db.Integer,
                                        db.ForeignKey('students.id', ondelete='CASCADE')),
                              db.Column('class_id', db.Integer,
                                        db.ForeignKey('classes.id', ondelete='CASCADE'))
                              )


class Students(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(255), nullable=False)
    last_name = db.Column(db.String(255), nullable=False)
    birthdate = db.Column(db.Date, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    house_id = db.Column(db.Integer, db.ForeignKey(
        'houses.id', ondelete='SET NULL'))
    registered_classes = db.relationship(
        "Classes", secondary=registration_table)


class Classes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    credit = db.Column(db.String(255), nullable=False)
    professor_id = db.Column(db.Integer, db.ForeignKey(
        'professors.id', ondelete='SET NULL'))


# route decorator tells Flask what URL should trigger our function. Just calling a website with url is a GET request.


@app.route('/')
def hi():              # function given a name, which is used to generate URLs for that function (url_for(hi))
    # return ("string")  OR render_template("page.html"), belonging in templates folder
    return redirect('/students')


@app.route('/students', methods=['POST', 'GET'])
def show_students():
    if request.method == "GET":
        students = Students.query.order_by(Students.last_name).all()
        houses = Houses.query.order_by(Houses.name).all()

        # for each student, get the name of their house from the house id
        student_houses = [Houses.query.filter_by(
            id=student.house_id).first() for student in students]
        for idx, house in enumerate(student_houses):
            student_houses[idx] = house.name if house else None

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

            try:
                db.session.add(new_student)
                db.session.commit()
                print(
                    f'POST: new student: {first_name} {last_name} successfully added')
            except:
                return("There was an error adding that student.")

            return redirect('/students')

        # delete 'post_type' == 'delete'
        else:
            print("\n------- index POST delete -----")
            print("deleting a student to the database")
            delete_id = request.form['delete_id']
            student_to_delete = Students.query.get_or_404(delete_id)
            try:
                print(
                    f"Deleting Student ID:{student_to_delete.id}, {student_to_delete.first_name} {student_to_delete.last_name}. ", end="")
                db.session.delete(student_to_delete)
                db.session.commit()
                print("Deletion Successful!")
            except:
                return("There was an error deleting that student.")

            return redirect('/students')


@app.route('/update-student/<int:id>', methods=['POST', 'GET'])
def update_student(id):
    if request.method == 'GET':
        student = Students.query.get_or_404(id)
        houses = Houses.query.order_by(Houses.name).all()
        return render_template('update_students.html', student=student, houses=houses)
    elif request.method == 'POST':
        # update values

        student_to_update = Students.query.get_or_404(id)
        print(
            f"updating values for: {student_to_update.id} {student_to_update.first_name} {student_to_update.last_name}")
        student_to_update.first_name = request.form['first_name']
        student_to_update.last_name = request.form['last_name']
        student_to_update.birthdate = request.form['birthdate']
        student_to_update.year = request.form['year']
        student_to_update.house_id = request.form['house_id']
        try:
            db.session.commit()
            print("Update Successful!")
        except:
            return "There was an error updating the student"
        return redirect('/students')


@app.route('/houses', methods=['POST', 'GET'])
def show_houses():
    if request.method == "GET":
        houses = Houses.query.order_by(Houses.name).all()
        return render_template('houses.html', houses=houses,)
    elif request.method == "POST":
        if request.form['post_type'] == "add":
            print("\n------- index POST add -----")
            print("Adding a house to the database")

            name = request.form['name']
            mascot = request.form['mascot']
            founder = request.form['founder']
            head = request.form['head']

            new_house = Houses(
                name=name, mascot=mascot, founder=founder, head=head)

            try:
                db.session.add(new_house)
                db.session.commit()
                print(
                    f'POST: new house: {name} successfully added')
            except:
                return("There was an error adding that house.")

            return redirect('/houses')

        # delete 'post_type' == 'delete'
        else:
            print("\n------- index POST delete -----")
            print("deleting a house to the database")
            delete_id = request.form['delete_id']
            house_to_delete = Houses.query.get_or_404(delete_id)
            try:
                print(
                    f"Deleting House ID:{house_to_delete.id}, {house_to_delete.name} {house_to_delete.mascot}. ", end="")
                db.session.delete(house_to_delete)
                db.session.commit()
                print("Deletion Successful!")
            except:
                return("There was an error deleting that house.")

            return redirect('/houses')


@app.route('/update-house/<int:id>', methods=['POST', 'GET'])
def update_house(id):
    if request.method == 'GET':
        house = Houses.query.get_or_404(id)
        return render_template('update_houses.html', house=house)
    elif request.method == 'POST':
        # update values
        house_to_update = Houses.query.get_or_404(id)
        print(
            f"updating values for: {house_to_update.id} {house_to_update.name} {house_to_update.mascot}")
        house_to_update.name = request.form['name']
        house_to_update.mascot = request.form['mascot']
        house_to_update.founder = request.form['founder']
        house_to_update.head = request.form['head']
        try:
            db.session.commit()
            print("Update Successful!")
        except:
            return "There was an error updating the house"
        return redirect('/houses')


@app.route('/professors', methods=['POST', 'GET'])
def show_professors():
    if request.method == "GET":
        professors = Professors.query.order_by(Professors.last_name).all()
        houses = Houses.query.order_by(Houses.name).all()

        # for each professor, get the name of their house from the house id
        professor_houses = [Houses.query.filter_by(
            id=professor.house_id).first() for professor in professors]
        for idx, house in enumerate(professor_houses):
            professor_houses[idx] = house.name if house else None

        return render_template('professors.html', professors=professors, houses=houses, professor_houses=professor_houses)

    elif request.method == "POST":
        if request.form['post_type'] == "add":
            print("\n------- index POST add -----")
            print("Adding a professor to the database")

            first_name = request.form['first_name']
            last_name = request.form['last_name']
            house_id = request.form['house_id']

            print("PARAMS:", first_name, last_name, house_id)

            new_professor = Professors(
                first_name=first_name, last_name=last_name, house_id=house_id)

            # try:
            db.session.add(new_professor)
            db.session.commit()
            print(
                f'POST: new professor: {first_name} successfully added')
            # except:
            #     "There was an error adding that professor."

            return redirect('/professors')

        # delete 'post_type' == 'delete'
        else:
            print("\n------- index POST delete -----")
            print("deleting a professor to the database")
            delete_id = request.form['delete_id']
            professor_to_delete = Professors.query.get_or_404(delete_id)
            try:
                print(
                    f"Deleting Professor ID:{professor_to_delete.id}, {professor_to_delete.first_name} {professor_to_delete.last_name}. ", end="")
                db.session.delete(professor_to_delete)
                db.session.commit()
                print("Deletion Successful!")
            except:
                return("There was an error deleting that professor.")

            return redirect('/professors')


@app.route('/update-professor/<int:id>', methods=['POST', 'GET'])
def update_professor(id):
    if request.method == 'GET':
        professor = Professors.query.get_or_404(id)
        houses = Houses.query.order_by(Houses.name).all()
        return render_template('update_professors.html', professor=professor, houses=houses)
    elif request.method == 'POST':
        # update values

        professor_to_update = Professors.query.get_or_404(id)
        print(
            f"updating values for: {professor_to_update.id} {professor_to_update.first_name} {professor_to_update.last_name}")
        professor_to_update.first_name = request.form['first_name']
        professor_to_update.last_name = request.form['last_name']
        professor_to_update.house_id = request.form['house_id']
        try:
            db.session.commit()
            print("Update Successful!")
        except:
            return "There was an error updating the professor"
        return redirect('/professors')


@app.route('/classes', methods=['POST', 'GET'])
def show_classes():
    if request.method == 'GET':
        courses = Classes.query.order_by(Classes.name).all()
        professors = Professors.query.order_by(Professors.last_name).all()

        # for each course, get the name of their professor from the professor id
        course_professors = [Professors.query.filter_by(
            id=course.professor_id).first() for course in courses]
        for idx, professor in enumerate(course_professors):
            course_professors[idx] = professor.last_name + \
                ", " + professor.first_name if professor else None
        return render_template('classes.html', courses=courses, professors=professors, course_professors=course_professors)
    elif request.method == 'POST':
        if request.form['post_type'] == "add":
            print("\n------- index POST add -----")
            print("Adding a class to the database")

            name = request.form['name']
            credit = request.form['credit']
            professor_id = request.form['professor_id']

            new_class = Classes(
                name=name, credit=credit, professor_id=professor_id)

            try:
                db.session.add(new_class)
                db.session.commit()
                print(
                    f'POST: new class: {name}  successfully added')
            except:
                return("There was an error adding that class.")

            return redirect('/classes')

        # delete 'post_type' == 'delete'
        else:
            print("\n------- POST delete -----")
            print("deleting a class from the database")
            delete_id = request.form['delete_id']
            class_to_delete = Classes.query.get_or_404(delete_id)
            try:
                print(
                    f"Deleting Class ID: {class_to_delete.id}, Name: {class_to_delete.name}. ", end="")
                db.session.delete(class_to_delete)
                db.session.commit()
                print("Deletion Successful!")
            except:
                return("There was an error deleting that class.")

            return redirect('/classes')


@app.route('/update-class/<int:id>', methods=['POST', 'GET'])
def update_class(id):
    if request.method == 'GET':
        course = Classes.query.get_or_404(id)
        professors = Professors.query.order_by(Professors.last_name).all()
        return render_template('update_classes.html', course=course, professors=professors)
    elif request.method == 'POST':
        # update values
        class_to_update = Classes.query.get_or_404(id)
        print(
            f"updating values for: ID: {class_to_update.id} Name: {class_to_update.name}...")
        class_to_update.name = request.form['name']
        class_to_update.credit = request.form['credit']
        class_to_update.professor_id = request.form['professor_id']
        try:
            db.session.commit()
            print("Update Successful!")
        except:
            return "There was an error updating the class"
        return redirect('/classes')


@app.route('/registrations', methods=['POST', 'GET'])
def show_registrations():
    if request.method == 'GET':
        registrations = db.session.query(registration_table).all()
        students_courses = []
        for registration in registrations:
            student_id = registration.student_id
            student = Students.query.get_or_404(student_id)

            class_id = registration.class_id
            course = Classes.query.get_or_404(class_id)
            # list of tuples of (student_entry, course_entry)
            students_courses.append((student, course))
        students = Students.query.order_by(Students.last_name).all()
        courses = Classes.query.order_by(Classes.name).all()
        return render_template('registrations.html', students_courses=students_courses, students=students, courses=courses)

    elif request.method == 'POST':
        if request.form['post_type'] == 'add':
            print("\n------- registration POST add -----")
            print("Adding a registration to the database")

            student_id = request.form['student_id']
            student = Students.query.get_or_404(student_id)

            course_id = request.form['course_id']
            course = Classes.query.get_or_404(course_id)

            try:
                print(
                    f'about to append registration, Student: {student.first_name} register Class: {course.name}')
                student.registered_classes.append(course)
                db.session.add(student)
                db.session.commit()
                print(f'POST: registration  successfully added')
            except:
                return("There was an error adding that registration .")

            return redirect('/registrations')

        #  delete a registration, 'post_type' == 'delete'
        else:
            print("\n------- POST delete -----")
            print("deleting a registration from the database")
            student_id = request.form['student_id']
            student = Students.query.get_or_404(student_id)

            class_id = request.form['class_id']
            course = Classes.query.get_or_404(class_id)

            try:
                print(
                    f"attempting to remove {student.first_name}'s registration of {course.name}")
                student.registered_classes.remove(course)
                db.session.commit()
                print('Successful removal of registration!')

            except:
                return("There was an error deleting that student-class registration.")

            return redirect('/registrations')
