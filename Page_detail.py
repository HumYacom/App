from flask import Blueprint, render_template, request, url_for, redirect, session
import pymysql
from dbconnect import *

db = pymysql.connect(host=HOST, user=USER, password=PASS, database=DATABASE)


detailpd = Blueprint('detailpd', __name__)


@detailpd.route("/detail_product",methods = ["GET"])
def detail_product():
    args = request.args
    data = args.get('no')
    with db.cursor() as cur:
        sql = "SELECT record.re_no, record.User_name, record.re_pstatus, record.Product_type, record.re_unit, Products.Product_manner, record.re_date, inventory.type_id, record.re_status FROM ((Products INNER JOIN inventory ON Products.Product_type = inventory.Product_type) INNER JOIN record ON Products.Product_type = requisition.Product_type) WHERE requisition.re_no = %s;"
        try:
            cur.execute(sql,(data))
            db.commit()
        except:
            return render_template('detail/detailPD.html', datas=('nodata'))
        rows = cur.fetchall()
    return render_template('detail/detailPD.html', datas=rows)
