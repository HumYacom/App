from flask import Blueprint, render_template, request, url_for, redirect, session, flash
import pymysql
from dbconnect import *
from flask_paginate import Pagination, get_page_args

db = pymysql.connect(host=HOST, user=USER, password=PASS, database=DATABASE)


Pageuse = Blueprint('Pageuse', __name__)

@Pageuse.route("/userindex")
def userindex():
    with db.cursor() as cur:
        sql = "SELECT * FROM requisition"
        try:
            cur.execute(sql)
            db.commit()
        except:
            return render_template('user/index_user.html', datas=('nodata'))
        rows = cur.fetchall()
        user = list(range(len(rows)))
        total = len(user)
        page,per_page,offset = get_page_args(page_parameter='page',per_page_parameter='per_page')
        pagination_user = user[offset:offset+10]
        pagination_data = pagination_user
        pagination = Pagination(page=page, per_page=per_page, total=total, css_framework='bootstrap5')
    return render_template('user/index_user.html', datas=rows,page=page, per_page=per_page, Pagination=pagination, len=total, user=pagination_data)

    
@Pageuse.route("/cresher", methods=["POST"])
def cresher():
    if request.method == "POST":
        dstart = request.form['dstart']
        endstart = request.form['endstart']
        with db.cursor() as cur:
            sql = "SELECT * FROM requisition WHERE re_date BETWEEN %s AND %s"
            try:
                cur.execute(sql, (dstart, endstart))
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
        re_status = request.form['re_status']
        with db.cursor() as cur:
            sql = "INSERT INTO requisition (re_no,User_name,re_pstatus,Product_type,re_unit,re_date,re_status) VALUES (%s,%s,%s,%s,%s,%s,%s)"
            try:
                cur.execute(sql, (runum, User_name, re_pstatus,Product_type, re_unit, re_date, re_status))
                db.commit()
                flash(
                    "ได้ทำการส่งเรื่องขอวัสดุแล้วกำลังส่งข้อมูล...กรุณารอสักครู่ครับ")
            except:
                return redirect(url_for('Pageuse.userindex', status="wait"))

            return redirect(url_for('Pageuse.userindex', status="wait"))

    return render_template("user/Add_user.html", status="wait")
