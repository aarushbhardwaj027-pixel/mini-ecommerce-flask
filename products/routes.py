from flask import Blueprint,render_template,request,redirect,session
from models import db,User,Products,Order

product_bp = Blueprint('product',__name__)


# ________________________________add product________________________-
@product_bp.route('/add_product', methods=['GET', 'POST'])
def add_product():
    if 'user_id' not in session:
        return redirect("/")

    user = session['user_id']
    user1 = User.query.filter_by(id=user).first()

    if user1.role =="buyer":
        return redirect("/product/view")


    if request.method == 'POST' :
            product_name = request.form['product_name']
            product_description = request.form['product_description']
            price = int(request.form['price'])
            quantity = int(request.form['quantity'])

            product = Products(
                product_name=product_name,
                product_description=product_description,
                price=price,
                qty=quantity,
                user_id=user
            )

            db.session.add(product)
            db.session.commit()

            return redirect('/product')
    
    return render_template('add_product.html',user1 = user1)
# ________________________________view product________________________-

@product_bp.route('/view')
def view():
    if 'user_id' not in session:
        return redirect('/')
    else:
        products = Products.query.all()
        current_user = session['user_id']
        user = User.query.filter_by(id = current_user).first()
    
    return render_template('view.html',products = products,user = user)

# ________________________________view my product________________________-

@product_bp.route('/view-myproduct')
def view_my():
    if 'user_id' not in session:
        return redirect('/')
    else:
        current_user = session['user_id']
        user = User.query.filter_by(id = current_user).first()
        my_products = user.product
    
    return render_template('my-products.html',user = user,my_products = my_products)


# ________________________________order product________________________-

@product_bp.route('/order/<int:id>',methods = ['GET','POST'])
def order(id):
    if 'user_id' not in session:
        return redirect('/auth/login')

    user_id = session['user_id']

    product_buy =  Products.query.filter_by(id = id).first()

    if not product_buy:
        return "Product not found", 404
        
    if product_buy.qty >= 1:
        product_buy.qty -= 1

        order = Order.query.filter_by(
            product_id=id,
            user_id=user_id,
            paid=False
        ).first()
            
        if order:
            order.qty += 1
                
        else:
            Order1 = Order(product_id = id,user_id = user_id , qty = 1,paid = False)

            db.session.add(Order1)
                
        db.session.commit()

    else:
            
        return 'Out of stock'

    return redirect('/product/view')
# ________________________________view orders________________________-
@product_bp.route('/view-myorder')
def view_order():
    if 'user_id' not in session:
        return redirect("/auth/login")
    
    user_id = session['user_id']

    my_order = Order.query.filter_by(user_id=user_id, paid=False).all()

    price = 0

    for x in my_order:
        price +=  x.product.price * x.qty

    return render_template('my_order.html',my_order = my_order , price =price)
# ________________________________History________________________-

@product_bp.route('/view-history')
def view_history():
    if 'user_id' not in session:
        return redirect("/auth/login")

    user_id = session['user_id']

    history = Order.query.filter_by(user_id=user_id, paid=True).all()

    price = 0
    for x in history:
        price += x.product.price * x.qty

    return render_template('history.html', my_order=history, price=price)
# ________________________________Pay________________________-
@product_bp.route('/pay', methods=['POST'])
def pay():
    if 'user_id' not in session:
        return redirect('/auth/login')

    user_id = session['user_id']

    orders = Order.query.filter_by(user_id=user_id, paid=False).all()

    for order in orders:
        order.paid = True

    db.session.commit()

    return redirect('/product/view-myorder')

# ________________________________cancel orders________________________-
@product_bp.route('/cancel/<int:id>',methods = ['POST'])
def cancel(id):
    if 'user_id' not in session:
        return redirect('/auth/login')
    
    user_id = session['user_id']

    cancel_order = Order.query.filter_by(id = id , user_id = user_id).first()

    if not cancel_order:
        return 'No Order',404
    
    product = cancel_order.product
    product.qty += 1
    cancel_order.qty -= 1

    if cancel_order.qty == 0 :
        db.session.delete(cancel_order)

    db.session.commit()

    return redirect('/product/view-myorder')

# ________________________________update product________________________-

@product_bp.route('/update/<int:id>',methods = ['GET','POST'])
def update(id):
    if 'user_id' not in session:
        return redirect('/')
    
    product = Products.query.filter_by(id=id).first()

    if not product:
        return "Product not found", 404
    
    if product.user_id != session['user_id']:
         return redirect('/product')
    
    if request.method == 'POST':
        product.product_name = request.form['product_name']
        product.product_description = request.form['product_description']
        product.price = request.form['price']
        product.qty = request.form['quantity']

        db.session.commit()

        return redirect('/product')
    return render_template('update.html',product = product)

# ________________________________delete product________________________-

@product_bp.route('/delete/<int:id>',methods = ['POST'])
def delete(id):
    if 'user_id' not in session:
        return redirect('/')

    product = Products.query.filter_by(id=id).first()

    if not product:
        return "Product not found", 404
    
    if product.user_id != session['user_id']:
         return redirect('/product')
    
    if not Order.query.filter_by(product_id=product.id).first():

        db.session.delete(product)
        db.session.commit()

    else:
         
         return redirect('/product')

    return redirect('/product/view')
    