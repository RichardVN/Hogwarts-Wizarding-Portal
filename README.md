# Witchcraft-School-Admin
A full stack CRUD web application to handle school administration tasks. Handle data of professors, students and more (in the flavor of Harry Potter!)

## Visit the Website
https://witchcraft-school-admin.herokuapp.com/
### Disclaimer
(This website is not endorsed or supported directly or indirectly with Warner Bros. Entertainment, JK Rowling, Pottermore, or any of the official Harry Potter trademark/right holders. It is used purely for non-commercial purposes only.)
## Techonologies Used:
Frontend: CSS3, HTML5, Javascript, Jinja2, Bootstrap4
Backend: Python(Flask), SQLAlchemy ORM
Database: PostgreSQL
## Features
- Full CRUD (Create, Read, Update, Delete) for Professors, Students, Classes, and Houses entities.
- Add student registrations, or drop students from registered classes
## Installation
Clone the repository `git clone https://github.com/RichardVN/Hogwarts-Wizarding-Portal.git`

If you don't have pipenv installed, run `pip install pipenv`

Create the Virtual environment and install dependencies `pipenv install`

Enter virtual environment `pipenv shell`

Run flask app on localhost `flask run`

Exit virtual environment `exit`

## Configuration
Adjust the variables in `.env.example` and then rename the file into `.env`

Set `FLASK_ENV` to `"development"` to turn on debug.

Set `FLASK_APP` to the py module to run as app's WSGI

Set the PostgreSQL credentials to connect to PostgreSQL database.
