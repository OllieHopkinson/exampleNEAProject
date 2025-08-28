#CRUD - create, retrive, update, delete

from flask import Blueprint, flash, redirect, request, session, url_for

from blueprints import pages
from database import databaseHandler

tasks = Blueprint('tasks', __name__, url_prefix='/tasks')

@tasks.route('/create', methods = ['POST'])
def createTask():
    formDetails = request.form
    taskName = formDetails.get('taskName')
    description = formDetails.get('description')
    userID = session['userID']
    errors = False

    if len(taskName) < 3:
        errors = True
        flash('invalid task name')

    if len(description) < 1:
        errors = True 
        flash('invalid task description')

    if errors:
        return redirect(url_for('pages.createTask'))
    
    db = databaseHandler()
    success, userID = db.createTask(taskName, description, userID)
    
    if success:
        return redirect(url_for('pages.dashboard'))
    
    flash('an error occurd making the task')
    return redirect(url_for('pages.createTask'))

# @tasks.route('/get')
# def getTasks():
#     return 'getting all tasks'

@tasks.route('/get/<int:taskID>')
def getTaskByID(taskID):
    return 'getting a tasks for task ID' + str(taskID)

@tasks.route('/update/<int:taskID>')
def updateTask(taskID):
    return 'updating task' + str(taskID)

@tasks.route('/updateStatus/<int:taskID>', methods = ['POST'])
def updateStatus(taskID):
    db = databaseHandler()
    userID = session['userID']

    success = db.updateStatus(taskID, userID)
    
    if not success:
        flash('task not updated successfully')

    return redirect(url_for('pages.dashboard'))

@tasks.route('/delete/<int:taskID>', methods = ['POST'])
def deleteTask(taskID):

    db = databaseHandler()
    userID = session['userID']
    success = db.deleteTask(taskID, userID)

    if not success:
        flash('task not dlelted')

    else:
        flash('task deleted successfully')

    return redirect(url_for('pages.dashboard'))
