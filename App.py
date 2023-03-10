from flask import Flask,render_template,request
from Page_login import *
from Page_user import *
from Page_admin import *
from Page_detail import *

app = Flask(__name__)
app.secret_key = "Administrator"
app.register_blueprint(User)
app.register_blueprint(Pageuse)
app.register_blueprint(Document_products)
app.register_blueprint(detailpd)

@app.route('/')
def index():
    return redirect(url_for('Pageuse.userindex'))

@app.route('/adminlog')
def adminlog():
    return redirect(url_for('Document_products.Admin_index'))

if __name__ == "__main__":
    app.run(debug=True)