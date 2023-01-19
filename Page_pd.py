from flask import Blueprint, render_template, request, url_for, redirect,session,flash
import pymysql
from dbconnect import *
from flask_paginate import Pagination, get_page_args

db = pymysql.connect(host=HOST, user=USER, password=PASS, database=DATABASE)


PD = Blueprint('PD', __name__)

@PD.route("/pd")
def pd():
    with db.cursor() as cur:
        sql = "SELECT Products.Product_id, Products.Product_name, inventory.Product_category, Products.Product_manner, Products.Product_price,Products.Product_date,inventory.type_id,inventory.Product_status FROM Products INNER JOIN inventory ON Products.Product_type = inventory.Product_type;"
        try:
            cur.execute(sql)
            db.commit()
        except:
            return render_template('admin/menu_pd.html', datas=('nodata'))
        rows = cur.fetchall()

        return render_template('admin/menu_pd.html', datas=rows)

@PD.route("/PD_edit", methods=["POST"])
def PD_edit():
    if request.method == "POST":
        runum = request.form['Product_id']
        User_name = request.form['Product_name']
        re_pstatus = request.form['Product_type']
        Product_type = request.form['Product_manner']
        re_unit = request.form['Product_price']
        re_date = request.form['Product_date']
        re_status = request.form['type_id']
        Product_status = request.form['Product_status']
        Product_category = request.form['Product_category']
        with db.cursor() as cur:
            sql = ""
            try:
                cur.execute(sql, (User_name, re_pstatus, Product_type, re_unit, re_status, runum, re_date, Product_status))
                db.commit()
            except:
                return redirect(url_for('PD.pd'))

            return redirect(url_for('PD.pd'))

    return redirect(url_for('PD.pd'))


@PD.route("/PD_del", methods=["POST"])
def PD_del():
    if request.method == "POST":
        No = request.form['Product_id']
        with db.cursor() as cur:
            sql = "DELETE FROM inventory WHERE Product_type = %s"
            sql2 = "DELETE FROM Products WHERE Product_id = %s"
            try:
                cur.execute(sql,(No))
                db.commit()
                cur.execute(sql2,(No))
                db.commit()
            except:
                return redirect(url_for('PD.pd'))

            return redirect(url_for('PD.pd'))

    return redirect(url_for('PD.pd'))

@PD.route("/PDadding")
def PDadding():
    return render_template("admin/PD_add.html")


@PD.route("/PDAdd", methods=["POST"])
def PDAdd():
    if request.method == "POST":
        runum = request.form['Product_id']
        User_name = request.form['Product_name']
        re_pstatus = request.form['Product_type']
        Product_type = request.form['Product_manner']
        re_unit = request.form['Product_price']
        re_date = request.form['Product_date']
        re_status = request.form['type_id']
        Product_status = request.form['Product_status']
        Product_category = request.form['Product_category']
        with db.cursor() as cur:
            sql = "INSERT INTO inventory(Product_category,type_id,Product_type,Product_status) VALUES(%s,%s,%s,%s)"
            sql2 = "INSERT INTO products(Product_id,Product_name,Product_type,Product_manner,Product_price,Product_date,type_id) VALUES(%s,%s,%s,%s,%s,%s,%s)"
            try:
                cur.execute(sql,(re_pstatus,re_status,Product_status,Product_category))
                db.commit()
                cur.execute(sql2,(runum,User_name,re_pstatus,Product_type,re_unit,re_date,re_status))
                db.commit()
                flash(
                    "ได้ทำการส่งเรื่องขอวัสดุแล้วกำลังส่งข้อมูล...กรุณารอสักครู่ครับ")
            except:
                return redirect(url_for('PD.pd', status="wait"))

            return redirect(url_for('PD.pd', status="wait"))

    return render_template("admin/PD_add.html", status="wait")