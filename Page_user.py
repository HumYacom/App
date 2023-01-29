from flask import Blueprint, render_template, request, url_for, redirect, session, flash
import pymysql
from dbconnect import *
from flask_paginate import Pagination, get_page_args

db = pymysql.connect(host=HOST, user=USER, password=PASS, database=DATABASE)


Pageuse = Blueprint('Pageuse', __name__)

@Pageuse.route("/userindex")
def userindex():
    with db.cursor() as cur:
        sql = "SELECT * FROM record ORDER BY re_date DESC"
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
        pagination_date = pagination_user
        pagination = Pagination(page=page, per_page=per_page, total=total, css_framework='bootstrap5')
    return render_template('user/index_user.html', datas=rows, page=page, per_page=per_page, Pagination=pagination, len=total, user=pagination_date)

    
@Pageuse.route("/cresher", methods=["POST"])
def cresher():
    if request.method == "POST":
        dstart = request.form['dstart']
        endstart = request.form['endstart']
        with db.cursor() as cur:
            sql = "SELECT * FROM record WHERE re_date BETWEEN %s AND %s"
            try:
                cur.execute(sql, (dstart, endstart))
                db.commit()
            except:
                return render_template('user/index_user.html', datas=('nodata'))
            rows = cur.fetchall()
            user = list(range(len(rows)))
            pagination_user = user
            pagination = Pagination(css_framework='bootstrap5')
        return render_template('user/index_user.html', datas=rows, Pagination=pagination, user=pagination_user)

@Pageuse.route("/cresher2", methods=["POST"])
def cresher2():
    if request.method == "POST":
        dfname = request.form['dfname']
        with db.cursor() as cur:
            sql = "SELECT * FROM record WHERE User_name = %s"
            try:
                cur.execute(sql, (dfname))
                db.commit()
            except:
                return render_template('user/index_user.html', datas=('nodata'))
            rows = cur.fetchall()
            user = list(range(len(rows)))
            pagination_user = user
            pagination = Pagination(css_framework='bootstrap5')
        return render_template('user/index_user.html', datas=rows, Pagination=pagination, user=pagination_user)

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
            sql = "INSERT INTO record (re_no,User_name,re_pstatus,Product_type,Product_export,re_date,re_status) VALUES (%s,%s,%s,%s,%s,%s,%s)"
            sql2 = "UPDATE record SET Product_export = Product_export - %s  WHERE re_no = %s;"
            sql3 = "SELECT Product_quantity, Product_id FROM products WHERE Product_type = %s"
            sql5 = "INSERT INTO borrow (borrow_no,Product_type,borrow_date,borrow_unit,User_name) VALUES (%s,%s,%s,%s,%s)"
            try:
                cur.execute(sql, (runum, User_name, re_pstatus,Product_type, re_unit, re_date, re_status))
                db.commit()
                cur.execute(sql2, (re_unit,runum))
                db.commit()
                cur.execute(sql3, (Product_type))
                db.commit()
                cur.execute(sql5, (runum,Product_type,re_date,re_unit,User_name))
                db.commit()
                
                rows = cur.fetchall()
                sql4 = "UPDATE products SET Product_quantity = Product_quantity - %s WHERE Product_id = %s"
                cur.execute(sql4, (re_unit,rows[0][1]))
                db.commit()
                flash(
                    "ได้ทำการส่งเรื่องขอวัสดุแล้วกำลังส่งข้อมูล...กรุณารอสักครู่ครับ")
            except:
                return redirect(url_for('Pageuse.userindex', status="wait"))

            return redirect(url_for('Pageuse.userindex', status="wait"))

    return render_template("user/Add_user.html", status="wait")
