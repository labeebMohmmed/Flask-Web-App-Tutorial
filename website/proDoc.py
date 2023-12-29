from flask import Blueprint, render_template, request, flash, jsonify, session, redirect,url_for
from .database import AuthenticationsDB
from datetime import date

proDoc = Blueprint('proDoc', __name__)
authDB = AuthenticationsDB()

@proDoc.route('home/authenticationsList', methods=['GET', 'POST'])
def authentications():
    authList = authDB.getTodaysList(date.today())    
    if 'loggedin' in session:
        if request.method == 'POST':  
            jobPosition = request.form.get('jobPosition')
            session['proType'] = jobPosition  
            return redirect(url_for('proDoc.newproDoc')) 
    else: 
        return redirect(url_for('login'))  
    return render_template("authenticationsList.html", authsList=authList)

@proDoc.route('home/authenticationsList/newproDoc', methods=['GET', 'POST'])
def newproDoc():       
    session['proCode'] = 12 
    flash(session['proType'], category='success') 
    return render_template("newproDoc.html")