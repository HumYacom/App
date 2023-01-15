from flask import Flask,render_template,request
from Page_login import *
from Page_user import *
from Page_admin import *
from datetime import timedelta

app = Flask(__name__)
app.secret_key = "Administrator"
app.permanent_session_lifetime = timedelta(days=1)
app.register_blueprint(User)
app.register_blueprint(Pageuse)
app.register_blueprint(Document_products)

@app.route('/')
def index():
    return redirect(url_for('Pageuse.userindex'))

@app.route('/adminlog')
def adminlog():
    return redirect(url_for('Document_products.Admin_index'))

if __name__ == "__main__":
    app.run(debug=True)