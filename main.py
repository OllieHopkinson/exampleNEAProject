from flask import Flask, get_flashed_messages, render_template, request, flash, redirect, url_for, session
from scripts.isAuthorised import isAuthorised
from database import databaseHandler
from blueprints.pages import pages
from blueprints.auth import auth
from blueprints.tasks import tasks

app = Flask(__name__)
app.secret_key = 'your-secret-key'
app.register_blueprint(pages)
app.register_blueprint(auth)
app.register_blueprint(tasks)

db = databaseHandler()
db.createTable()

app.run(debug = True)