

from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from .database import ItemDatabase
from datetime import date
auth = Blueprint('auth', __name__)

dirdb = ItemDatabase()

@auth.route('/login', methods=['GET', 'POST'])
def login():  
      
    if request.method == 'POST':
        userName = request.form.get('userName')
        password = request.form.get('password')
        user = dirdb.chech_user(userName)
        if user:
            
            if user['Aproved'] == 'نشط':
                if check_password_hash(user["Pass"], password):
                #if user["Pass"] == password:
                    print("arab name = " + user['arabName'] )
                    session['loggedin'] = True
                    session['userid'] = user['ID']
                    session['name'] = user['arabName']  
                    session['superAdmin'] = user['role']
                    return redirect(url_for('views.home'))
                else:
                    flash('خطأ في كلمة المرور', category='error')
            else:
                flash('الحساب لم يتم تفعيله حتى الان', category='error')
        else:
            flash('لا يوجد حساب باسم المسنخدم', category='error')

    return render_template("login.html")


@auth.route('/logout')
@login_required
def logout():
    session['loggedin'] = None
    session['userid'] = None
    session['name'] = None
    session['superAdmin'] = None
    return redirect(url_for('auth.login'))


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        body = {}                
        if request.method == 'POST': 
            body["greDate"] = date.today()
            body["role"] = "مستخدم"
            body["Aproved"] = "غير نشط"
            body["userName"] = request.form.get('userName')
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
            body["Pass"] =generate_password_hash(request.form.get('password1')) 
            password1 = request.form.get('password1') 
            password2 = request.form.get('password2') 
              
        if dirdb.chech_userName_arabName(body = body):
            flash('يوجد حساب باسم المستخدم أو اسم الموظف مسبقا، يرجى اختيار اسم آخر', category='error')
        elif len(body["userName"]) < 4 or len(body["userName"]) > 8:
            flash('اسم المستخدم يجب ان لا يقل عن اربعة احرف وان لا يزيد عن ثمانية.', category='error')
        elif body["arabName"].count(' ') < 2 or body["engName"].count(' ') < 2:
            flash('يجب ان يكون ان اسم الوظف ثلاثيا أو رباعيا باللغتين', category='error')
        elif password1 != password2:
            flash('كلمتي المرور غير متطابقتين', category='error')
        elif len(password1) < 3 or len(password1) > 10:
            flash('يجب أن لا تقل كلمة المرور عن ثمانية رموز وان لا تزي عن عشرة.', category='error')
        else:    
            dirdb.UserSignUp(body=body)        
            flash('تم تسجيل الحساب بنجاح، يرجى التواصل مع مدير القسم لتفعيل الحساب', category='success')
            return redirect(url_for('auth.login'))

    return render_template("sign_up.html")
