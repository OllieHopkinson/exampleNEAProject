from flask import Blueprint, flash, redirect, request, session, url_for
from database import databaseHandler

auth = Blueprint('auth', __name__, url_prefix='/auth')

@auth.route('/createuser', methods = ['POST'])
def createUser():
    formDetails = request.form
    username = formDetails.get('username')
    password = formDetails.get('password')
    repassword = formDetails.get('repassword')
    errors = False
            
    if password != repassword:
        flash('passwords dont match')
        errors = True
    
    if len(password) < 8:
        flash('password must equal 8 or more passwords')
        errors = True

    if len(username) < 3:
        flash('username must be 3 or more characters')
        errors = True

    if errors:
        return redirect(url_for('pages.signUp'))
        

    if password == repassword:
        if len(username) > 2 and len(password) > 7 and len(repassword) > 7 and password == repassword:
            db = databaseHandler()
            success, errorType = db.createUser(username, password)
            if success:
                return redirect(url_for('pages.dashboard'))
    
    if errorType == 'integrity-error':
        flash('invalid data has been entered please try again')
    elif errorType == 'unique-error':
        flash('username taken please use another')
    else:
        flash('unknown error occoured')

    return redirect(url_for('pages.signUp'))
         
    
@auth.route('/authoriseuser', methods = ['POST'])
def authoriseUser():
    formDetails = request.form
    username = formDetails.get('username')
    password = formDetails.get('password')

    db = databaseHandler()
    success, userID = db.authoriseUser(username, password)
    if success:
        session['currentUser'] = username
        session['userID'] = userID
        return redirect(url_for('pages.dashboard'))
    
    return redirect(url_for('pages.signIn'))


@auth.route('/signout')
def signOut():
    session.clear()
    return redirect(url_for('pages.signIn'))    
    