from flask import Blueprint, render_template, request, url_for, redirect,session,flash
import pymysql
from dbconnect import *
from flask_paginate import Pagination, get_page_args

db = pymysql.connect(host=HOST, user=USER, password=PASS, database=DATABASE)


Document_products = Blueprint('Document_products', __name__)


@Document_products.route("/Admin_index")
def Admin_index():
    if "username" not in session:
        return render_template('login.html')
    with db.cursor() as cur:
        sql = "SELECT * FROM record ORDER BY re_date DESC"
        try:
            cur.execute(sql)
            db.commit()
        except:
            return render_template('admin/index.html', datas=('nodata'))
        rows = cur.fetchall()
        user = list(range(len(rows)))
        total = len(user)
        page,per_page,offset = get_page_args(page_parameter='page',per_page_parameter='per_page')
        pagination_user = user[offset:offset+10]
        pagination_date = pagination_user
        pagination = Pagination(page=page, per_page=per_page, total=total, css_framework='bootstrap5')
    return render_template('admin/index.html', datas=rows, page=page, per_page=per_page, Pagination=pagination, len=total, user=pagination_date)

@Document_products.route("/cresheradmin", methods=["POST"])
def cresheradmin():
    if request.method == "POST":
        dstart = request.form['dstart']
        with db.cursor() as cur:
            sql = "SELECT * FROM record WHERE re_pstatus = %s"
            try:
                cur.execute(sql, (dstart))
                db.commit()
            except:
                return render_template('admin/index.html', datas=('nodata'))
            rows = cur.fetchall()
            user = list(range(len(rows)))
            pagination_user = user
            pagination = Pagination(css_framework='bootstrap5')
        return render_template('admin/index.html', datas=rows, Pagination=pagination, user=pagination_user)

@Document_products.route("/Admin_edit", methods=["POST"])
def Admin_edit():
    if request.method == "POST":
        No = request.form['re_no']
        User_name = request.form['User_name']
        re_pstatus = request.form['re_pstatus']
        Product_type = request.form['Product_type']
        re_unit = request.form['re_unit']
        re_status = request.form['re_status']

        with db.cursor() as cur:
            sql = "UPDATE record SET User_name = %s, re_pstatus = %s ,Product_type = %s, Product_export = %s, re_date = CURRENT_TIME(), re_status = %s WHERE re_no = %s"
            sql2 = "UPDATE record SET Product_export = Product_export - %s  WHERE re_no = %s;"
            sql3 = "SELECT Product_quantity, Product_id FROM products WHERE Product_type = %s"
            try:
                cur.execute(sql, (No, User_name, re_pstatus,Product_type, re_unit ,re_status))
                db.commit()
                cur.execute(sql2, (re_unit,No))
                db.commit()
                cur.execute(sql3, (Product_type))
                db.commit()
                
                rows = cur.fetchall()
                sql4 = "UPDATE products SET Product_quantity = Product_quantity + %s WHERE Product_id = %s"
                cur.execute(sql4, (re_unit,rows[0][1]))
                db.commit()
            
            except:
                return redirect(url_for('Document_products.Admin_index'))

            return redirect(url_for('Document_products.Admin_index'))

    return redirect(url_for('Document_products.Admin_index'))


@Document_products.route("/Admin_del", methods=["POST"])
def Admin_del():
    if request.method == "POST":
        No = request.form['re_no']
        with db.cursor() as cur:
            sql = "DELETE FROM record WHERE re_no = %s "
            try:
                cur.execute(sql,(No))
                db.commit()
            except:
                return redirect(url_for('Document_products.Admin_index'))

            return redirect(url_for('Document_products.Admin_index'))

    return redirect(url_for('Document_products.Admin_index'))

#menu products
@Document_products.route("/pd")
def pd():
    with db.cursor() as cur:
        sql = "SELECT Products.Product_id, Products.Product_type, products_type.Product_category, Products.Product_manner, Products.Product_quantity, Products.Product_date,products_type.type_id,Product_status,Product_quantity AS total FROM Products INNER JOIN products_type ON Products.Product_type = products_type.Product_type ORDER BY Product_id desc;"
        try:
            cur.execute(sql)
            db.commit()
        except:
            return render_template('admin/menu_pd.html', datas=('nodata'))
        rows = cur.fetchall()

        return render_template('admin/menu_pd.html', datas=rows)

@Document_products.route("/PD_edit", methods=["POST"])
def PD_edit():
    if request.method == "POST":
        runum = request.form['Product_id']
        re_pstatus = request.form['Product_type']
        Product_type = request.form['Product_manner']
        re_unit = request.form['Product_price']
        re_status = request.form['type_id']
        Product_status = request.form['Product_status']
        Product_category = request.form['Product_category']
        with db.cursor() as cur:
            sql = "UPDATE Products SET Product_type = %s, Product_manner = %s, Product_quantity = %s, type_id = %s WHERE Product_id = %s"
            sql2 = "UPDATE products_type SET Product_type = %s, Product_category = %s, Product_status = %s WHERE type_id = %s"
            try:
                cur.execute(sql, (re_pstatus, Product_type, re_unit, re_status, runum))
                db.commit()
                cur.execute(sql2, (re_status, re_pstatus, Product_status, Product_category))
                db.commit()
            except:
                return redirect(url_for('Document_products.pd'))

            return redirect(url_for('Document_products.pd'))

    return redirect(url_for('Document_products.pd'))


@Document_products.route("/PD_del", methods=["POST"])
def PD_del():
    if request.method == "POST":
        No = request.form['Product_id']
        with db.cursor() as cur:
            sql = "DELETE FROM products_type WHERE type_id = %s"
            sql2 = "DELETE FROM Products WHERE Product_id = %s"
            try:
                cur.execute(sql,(No))
                db.commit()
                cur.execute(sql2,(No))
                db.commit()
            except:
                return redirect(url_for('Document_products.pd'))

            return redirect(url_for('Document_products.pd'))

    return redirect(url_for('Document_products.pd'))

@Document_products.route("/PDadding")
def PDadding():
    return render_template("admin/PD_add.html")


@Document_products.route("/PDAdd", methods=["POST"])
def PDAdd():
    if request.method == "POST":
        runum = request.form['Product_id']
        re_pstatus = request.form['Product_type']
        Product_type = request.form['Product_manner']
        re_unit = request.form['Product_price']
        re_date = request.form['Product_date']
        re_status = request.form['type_id']
        Product_status = request.form['Product_status']
        Product_category = request.form['Product_category']
        with db.cursor() as cur:
            sql = "INSERT INTO products_type(type_id,Product_type,Product_category,Product_status) VALUES(%s,%s,%s,%s)"
            sql2 = "INSERT INTO products(Product_id,Product_type,Product_manner,Product_quantity,Product_date,type_id) VALUES(%s,%s,%s,%s,%s,%s)"
            try:
                cur.execute(sql,(re_status,re_pstatus,Product_category,Product_status))
                db.commit()
                cur.execute(sql2,(runum,re_pstatus,Product_type,re_unit,re_date,re_status))
                db.commit()
                flash(
                    "??????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????...??????????????????????????????????????????????????????")
            except:
                return redirect(url_for('Document_products.pd', status="wait"))

            return redirect(url_for('Document_products.pd', status="wait"))

    return render_template("admin/PD_add.html", status="wait")

#menu rigister products
@Document_products.route("/menurigis")
def menurigis():
    with db.cursor() as cur:
        sql = "SELECT * FROM products_type"
        try:
            cur.execute(sql)
            db.commit()
        except:
            return render_template('admin/menu_pdregis.html', datas=('nodata'))
        rows = cur.fetchall()
        return render_template('admin/menu_pdregis.html', datas=rows)

#menu broken products

@Document_products.route("/menubroken")
def menubroken():
    with db.cursor() as cur:
        sql = "SELECT * FROM products_broken"
        try:
            cur.execute(sql)
            db.commit()
        except:
            return render_template('admin/menu_pdbroken.html', datas=('nodata'))
        rows = cur.fetchall()
        return render_template('admin/menu_pdbroken.html', datas=rows)

#Borrow
@Document_products.route("/Borrow")
def Borrow():
    return
    
#Chart.js
@Document_products.route("/chartjs")
def chartjs():
    try:
        with db.cursor() as cur:

            query_type = "select Product_type from record" # query product_type
            cur.execute(query_type)
            db.commit() # fetch up to date data

            query_type_data = cur.fetchall()

            # chart config
            chart_export = {}
            chart_import = {}

            # extract
            for type in query_type_data:
                chart_export.update(
                    {
                        str(type[0]): 0
                    }
                )

                chart_import.update(
                    {
                        str(type[0]): 0
                    }
                )


            for type_query in chart_export:
                query_export = "select SUM(Product_export) AS Sum\
                    from record\
                    where Product_type = %s"

                cur.execute(query_export, type_query)
                db.commit()

                sumary_export = cur.fetchall()
                chart_export[type_query] = int(sumary_export[0][0])

            for type_query in chart_export:
                query_import = "select SUM(Product_import) AS Sum\
                    from record\
                    where Product_type = %s"

                cur.execute(query_import, type_query)
                db.commit()

                sumary_import = cur.fetchall()
                chart_import[type_query] = int(sumary_import[0][0])

        return render_template('admin/chart.html' ,chart_import = chart_import, chart_export=chart_export)
    except:
        return render_template('admin/chart.html' ,chart_import = chart_import, chart_export=chart_export)