from flask import Blueprint, render_template, request, url_for, redirect, session
import pymysql
from dbconnect import *

db = pymysql.connect(host=HOST, user=USER, password=PASS, database=DATABASE)


Pageuse = Blueprint('Pageuse', __name__)


@Pageuse.route("/Userindex")
def userindex():
    with db.cursor() as cur:
        sql = "SELECT * FROM requisition"
        try:
            cur.execute(sql)
            db.commit()
        except:
            return render_template('user/index_user.html', datas=('nodata'))
        rows = cur.fetchall()
    return render_template('user/index_user.html', datas=rows)

@Pageuse.route("/Useradding")
def useradding():
    return render_template("user/Add_user.html")

@Pageuse.route("/userAdd", methods=["POST"])
def userAdd():
    if request.method == "POST":
        runum = request.form['re_no']
        User_name = request.form['User_name']
        re_pstatus = request.form['re_pstatus']
        Product_type = request.form['Product_type']
        re_unit = request.form['re_unit']
        re_date = request.form['re_date']
        with db.cursor() as cur:
            sql = "INSERT INTO requisition (re_no,User_name,re_pstatus,Product_type,re_unit,re_date) VALUES (%s,%s,%s,%s,%s,%s)"
            try:
                cur.execute(sql, (runum,User_name,re_pstatus,Product_type, re_unit, re_date))
                db.commit()
            except:
                return redirect(url_for('Pageuse.userindex'))

            return redirect(url_for('Pageuse.userindex'))

    return render_template("user/Add_user.html")
