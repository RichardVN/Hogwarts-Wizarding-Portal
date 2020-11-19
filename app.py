from flask import Flask, render_template

# create instance of Flask class, which acts as our Web Server Gateway Interface (WSGI) app
app = Flask(__name__)       # argument is name of the app's module. We use __name__ because we run as '__main__'

# route decorator tells Flask what URL should trigger our function
@app.route('/')
def hi():                       # function given a name, which is used to generate URLs for that function
    return render_template('base.html')    # return ("string")  OR render_template("page.html"), belonging in templates folder

@app.route('/index')
def index():
    title = "new title"
    names = ['alice', 'jessica', 'katie']
    return render_template('index.html', title=title, names=names)     # pass context from controller app to template html page KWARG

@app.route('/students', methods = ['POST', 'GET'])
def show_students():
    return render_template('students.html')

@app.route('/houses', methods = ['POST', 'GET'])
def show_houses():
    return render_template('houses.html')

@app.route('/professors', methods = ['POST', 'GET'])
def show_professors():
    return render_template('professors.html')

@app.route('/classes', methods = ['POST', 'GET'])
def show_classes():
    return render_template('classes.html')

@app.route('/registrations', methods = ['POST','GET'])
def show_registrations():
    return render_template('registrations.html')