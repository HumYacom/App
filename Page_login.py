from flask import Blueprint, render_template, request, url_for, redirect, session, flash
import pymysql
from dbconnect import *

db = pymysql.connect(host=HOST, user=USER, password=PASS, database=DATABASE)


User = Blueprint('User', __name__)


@User.route("/login")
def loginpage():
    if "username" not in session:
        return render_template("login/login.html")
    else:
        return redirect(url_for('Document_products.Admin_index'))

@User.route("/Checklog", methods=["POST"])
def Checklog():
    username = request.form['Userid']
    password = request.form['Password']

    with db.cursor() as cur:
        sql = "SELECT * FROM user WHERE User_log = %s AND User_pass = %s AND Status = 1 "
        try:
            cur.execute(sql, (username, password))
            db.commit()
        except:
            return render_template('admin/index.html', datas=('nodata'))
        rows = cur.fetchall()

        if len(rows) > 0:
            session['username'] = username
            session['Name'] = rows[0][1]
            session.permanent = True
            return redirect(url_for('Document_products.Admin_index'))
        else:
            flash("User or password ไม่ถูกต้อง")
            return render_template('login/login.html')
         

@User.route("/logout")
def logout():
    session.clear()
    return redirect(url_for('User.loginpage'))

@User.route("/Register")
def register():
    return render_template('login/register.html')

@User.route("/Adduser", methods = ["POST"])
def Adduser():
    if request.method == "POST":
        No = request.form['TextID']
        Name = request.form['Name']
        Username = request.form['Username']
        Password = request.form['Password']
        Re = request.form['Repassword']
        if Password != Re:
            flash("Password or Re-password not found")
            return render_template('login/register.html')
        with db.cursor() as cur:
            sql = "INSERT INTO user (User_id,User_name,User_log,User_pass) VALUES (%s,%s,%s,%s)"
            try:
                cur.execute(sql,(No,Name,Username,Password))
                db.commit()
                flash("welcome user wait admin request")
            except:
                             
                return render_template('login/login.html',status="wait")

            return render_template('login/login.html',status="wait")

    return render_template('login/login.html',status="wait")