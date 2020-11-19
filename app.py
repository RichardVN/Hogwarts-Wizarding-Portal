from flask import Flask, render_template

# create instance of Flask class, which acts as our Web Server Gateway Interface (WSGI) app
app = Flask(__name__)       # argument is name of the app's module. We use __name__ because we run as '__main__'

# route decorator tells Flask what URL should trigger our function
@app.route('/hello')
def hi():                       # function given a name, which is used to generate URLs for that function
    return ("Hello World!!")    # return ("string")  OR render_template("page.html"), belonging in templates folder

