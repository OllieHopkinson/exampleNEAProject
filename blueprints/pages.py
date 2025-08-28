from flask import Blueprint, get_flashed_messages, redirect, render_template, session, url_for
from database import databaseHandler
from scripts.isAuthorised import isAuthorised

pages = Blueprint('pages', __name__)

@pages.route('/signup')
def signUp():
    messages = get_flashed_messages()
    return render_template('signup.html', messages = messages)

@pages.route('/dashboard')
def dashboard():
    if not isAuthorised():
        return redirect(url_for('pages.signIn'))
    
    currentUser = session['currentUser']
    userID = session['userID']

    db = databaseHandler()
    success, tasks = db.fetchAllTask(userID)

    messages = get_flashed_messages()

    return render_template('dashboard.html', currentUser = currentUser, tasks = tasks, messages = messages)

@pages.route('/')
def signIn():
    if isAuthorised():
        return redirect(url_for('pages.dashboard'))
    return render_template('signin.html')

@pages.route('/createTask')
def createTask():
    messages = get_flashed_messages()
    return render_template('createTask.html', messages = messages)