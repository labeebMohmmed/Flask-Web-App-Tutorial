from flask import Blueprint, render_template, request, flash, jsonify, session, redirect,url_for
from flask_login import login_required, current_user
from .models import Note
from .database import ItemDatabase,AuthenticationsDB
from . import db
import json
from werkzeug.security import generate_password_hash, check_password_hash
views = Blueprint('views', __name__)
usersDB = ItemDatabase()

@views.route('/users', methods = ['GET', 'POST'])
def userstest():
    flash('تم تحديث البيانات بنجاح', category='success') 
    return render_template('userslist.html')

@views.route('/users', methods = ['GET', 'POST'])
def users():
    if 'loggedin' in session:
        users = usersDB.get_Users()
        body = {}
        if request.method == 'POST':  
            body["id"] = int(request.form.get('userid'))       
            body["arabName"] = request.form.get('arabName')
            body["engName"] = request.form.get('engName')           
            body["sexOption"] = request.form.get('sexOption')
            body["isActive"] = request.form.get('isActive')  
            body["jobPosition"] = request.form.get('jobPosition')  
            body["role"] = request.form.get('role')  
            if body["jobPosition"] == "1":
                body["jobPosition"] = "قنصل عام"
            if body["jobPosition"] == "2":
                body["jobPosition"] = "نائب قنصل"
            if body["jobPosition"] == "3":
                body["jobPosition"] = "اداري"
            if body["jobPosition"] == "4":
                body["jobPosition"] = "مدير مالي"
            if body["jobPosition"] == "5":
                body["jobPosition"] = "محاسب"
            if body["jobPosition"] == "6":
                body["jobPosition"] = "موظف محلي"
            if  body["arabName"].count(' ') < 2 or  body["engName"].count(' ') < 2:
                flash('يجب ان يكون ان اسم الوظف ثلاثيا أو رباعيا باللغتين', category='error')        
            else:
                usersDB.UserUpdateUserInfo(body=body)
                flash('تم تحديث البيانات بنجاح', category='success') 
                return redirect(url_for('views.users'))  
    else:
        return redirect(url_for('login'))       
    return render_template('userslist.html', users = users)
    


@views.route('/view', methods = ['GET', 'POST'])
def view():
    if 'loggedin' in session:
        body = {}
        
        edituser = usersDB.get_User(session['userid'])        
        if request.method == 'POST': 
            body["id"] = int(request.form.get('userid'))
            body["arabName"] = request.form.get('arabName')
            body["engName"] = request.form.get('engName')
           
            body["sexOption"] = request.form.get('sexOption')
            body["isActive"] = request.form.get('isActive')  
            body["jobPosition"] = request.form.get('jobPosition')      
            if body["jobPosition"] == "1":
                body["jobPosition"] = "قنصل عام"
            if body["jobPosition"] == "2":
                body["jobPosition"] = "نائب قنصل"
            if body["jobPosition"] == "3":
                body["jobPosition"] = "اداري"
            if body["jobPosition"] == "4":
                body["jobPosition"] = "مدير مالي"
            if body["jobPosition"] == "5":
                body["jobPosition"] = "محاسب"
            if body["jobPosition"] == "6":
                body["jobPosition"] = "موظف محلي"

            if  body["arabName"].count(' ') < 2 or  body["engName"].count(' ') < 2:
                flash('يجب ان يكون ان اسم الوظف ثلاثيا أو رباعيا باللغتين', category='error')
        
            else:
                usersDB.AdminUpdateUserInfo(body=body)
                return redirect(url_for('views.users')) 
        return render_template('edit.html', edituser = edituser)
    return redirect(url_for('login')) 


@views.route('/userPref/userPersEdit', methods=['GET', 'POST'])
def userPersEdit():
    edituser = usersDB.get_User(session['userid'])   
    if 'loggedin' in session:
        body = {}                
        if request.method == 'POST': 
            body["id"] = int(session['userid'])
            body["arabName"] = request.form.get('arabName')
            body["engName"] = request.form.get('engName')           
            body["sexOption"] = request.form.get('sexOption')
            body["jobPosition"] = request.form.get('jobPosition')      
            if body["jobPosition"] == "1":
                body["jobPosition"] = "قنصل عام"
            elif body["jobPosition"] == "2":
                body["jobPosition"] = "نائب قنصل"
            elif body["jobPosition"] == "3":
                body["jobPosition"] = "اداري"
            elif body["jobPosition"] == "4":
                body["jobPosition"] = "مدير مالي"
            elif body["jobPosition"] == "5":
                body["jobPosition"] = "محاسب"
            elif body["jobPosition"] == "6":
                body["jobPosition"] = "موظف محلي"

            if  body["arabName"].count(' ') < 2 or  body["engName"].count(' ') < 2:
                flash('يجب ان يكون ان اسم الوظف ثلاثيا أو رباعيا باللغتين', category='error')
            else:    
                usersDB.UserUpdateUserInfo(body=body)
                flash('تم تحديث البيانات بنجاح', category='success') 
                return redirect(url_for('views.userPref')) 
    else:
        return redirect(url_for('auth.login')) 
    return render_template("userPersEdit.html" , edituser = edituser)


@views.route('/userPref/userPassEdit', methods=['GET', 'POST'])
def userPassEdit():        
    if 'loggedin' in session:
        userPass =  {}
        for row in usersDB.get_User(session['userid']):
            userPass["Pass"] = row[6]    
        print(userPass['Pass'])        
        if request.method == 'POST': 
            password = request.form.get('password')
            password1 = request.form.get('password1')
            password2 = request.form.get('password2')        
            if check_password_hash(userPass["Pass"], password):    
            #if password != userPass['Pass']:
                    
                flash('كلمة المرور غير مطابقة للكلمة الحالية، يرجى التواصل مع مدير النظام لاعادة ضبطها', category='error')
            elif password1 != password2:
                flash('كلمة المرور غير متطابقة', category='error')
            elif len(password1) < 3 or len(password1) > 10:
                flash('يجب أن لا تقل كلمة المرور عن ثمانية رموز وان لا تزي عن عشرة.', category='error')
            else:                              
                print("hash =" + generate_password_hash(password1))
                print(len(generate_password_hash(password1)))
                usersDB.UserUpdatePassword(newpass=generate_password_hash(password1), userid = int(session['userid']) )
                flash('تم تحديث كلمة المرور بنجاح', category='success') 
                return redirect(url_for('views.userPref')) 
    else:
        return redirect(url_for('auth.login')) 
    return render_template("userPassEdit.html")

@views.route('/userPref', methods=['GET', 'POST'])
def userPref():
    edituser = usersDB.get_User(session['userid'])   
    return render_template("userPref.html")

@views.route('/home', methods=['GET', 'POST'])
def home():
    
    return render_template("mainV.html")



@views.route('/delete-note', methods=['POST'])
def delete_note():  
    note = json.loads(request.data) # this function expects a JSON from the INDEX.js file 
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})


