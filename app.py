from flask import Flask,render_template,session,redirect
from auth.routes import auth_bp
from products.routes import product_bp
from models import db,Products,User
from extensions import cache

app = Flask(__name__)

app.config['SECRET_KEY'] = '10027927001'

cache.init_app(app, config={"CACHE_TYPE": "simple"})

app.config['SQLALCHEMY_DATABASE_URI'] = r'sqlite:///ecommerce.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.register_blueprint(auth_bp,url_prefix = '/auth')
app.register_blueprint(product_bp,url_prefix = '/product')

db.init_app(app)

@app.route('/')
@cache.cached(timeout=30)
def home():
    if 'user_id' in session:
        return redirect('/product')
    products = Products.query.all()
    return render_template("index.html",products = products) 


@app.route('/product')
def product():
    if 'user_id' not in session:
        return redirect('/')
    else:
        user_id = session['user_id']
        user = User.query.filter_by(id = user_id ).first()
        return render_template("products.html",user = user) 




with app.app_context():
    db.create_all() 

if __name__ == "__main__":
    app.run(debug=True)