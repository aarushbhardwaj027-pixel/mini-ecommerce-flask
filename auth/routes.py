from flask import render_template,request,redirect,Blueprint,session
from models import db,User
from werkzeug.security import check_password_hash,generate_password_hash
from sqlalchemy.exc import IntegrityError

auth_bp = Blueprint('auth',__name__)

# ____________________________________login_____________________________

@auth_bp.route('/login',methods = ['POST','GET'])
def login():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']

        role = request.form['choices']

        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password)  and user.email == email:
            session['user_id'] = user.id

            return redirect('/product')
        
        else:
            return redirect("/auth/login")

    return render_template('login.html')


# ____________________________________signup_____________________________

@auth_bp.route('/signup',methods = ['POST','GET'])
def signup():
    
    if request.method == "POST":
        username = request.form['username']
        email = request.form['email']

        password = str(request.form['password'])
        role = request.form['choices']

        current_user = User.query.filter(
            (User.username == username) | (User.email == email)
        ).first()

        if current_user:
            return redirect('/auth/signup')
        
        encoded = generate_password_hash(password, method='pbkdf2:sha256', salt_length=16)

        user1 = User(username=username,email =email,password = encoded,role = role)

        try:
            db.session.add(user1)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            return redirect('/auth/signup')

        return redirect('/auth/login')

    return render_template('signup.html')

# ____________________________________logout_____________________________

@auth_bp.route("/logout")
def logout():
    if 'user_id' in session:

        session.pop('user_id',None)
        return redirect("/")
    else:
        return redirect("/")