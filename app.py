from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from forms import CheckoutForm
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///grocery.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# import models after db init
from models import Product, Order, OrderItem

# --- helpers for cart (session) ---
def get_cart():
    return session.setdefault('cart', {})

def add_to_cart(product_id, qty=1):
    cart = get_cart()
    cart[str(product_id)] = cart.get(str(product_id), 0) + int(qty)
    session['cart'] = cart
    session.modified = True

def remove_from_cart(product_id):
    cart = get_cart()
    cart.pop(str(product_id), None)
    session['cart'] = cart
    session.modified = True

def clear_cart():
    session['cart'] = {}
    session.modified = True

def cart_items():
    cart = get_cart()
    items = []
    total = 0
    for pid, qty in cart.items():
        p = Product.query.get(int(pid))
        if not p:
            continue
        subtotal = p.price * qty
        items.append({'product': p, 'qty': qty, 'subtotal': subtotal})
        total += subtotal
    return items, total

# --- routes ---
@app.route('/')
def home():
    q = request.args.get('q', '')
    if q:
        products = Product.query.filter(Product.name.ilike(f'%{q}%')).all()
    else:
        products = Product.query.order_by(Product.id.desc()).all()
    return render_template('home.html', products=products, q=q)

@app.route('/product/<int:product_id>')
def product_detail(product_id):
    p = Product.query.get_or_404(product_id)
    return render_template('product_detail.html', product=p)

@app.route('/cart')
def view_cart():
    items, total = cart_items()
    return render_template('cart.html', items=items, total=total)

@app.route('/cart/add/<int:product_id>', methods=['POST'])
def cart_add(product_id):
    qty = int(request.form.get('qty', 1))
    add_to_cart(product_id, qty)
    flash('Mahsulot savatga qo‘shildi.', 'success')
    return redirect(request.referrer or url_for('home'))

@app.route('/cart/remove/<int:product_id>', methods=['POST'])
def cart_remove(product_id):
    remove_from_cart(product_id)
    flash('Mahsulot savatdan olib tashlandi.', 'info')
    return redirect(url_for('view_cart'))

@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    items, total = cart_items()
    if not items:
        flash('Savat bo‘sh - avval mahsulot qo‘shing.', 'warning')
        return redirect(url_for('home'))

    form = CheckoutForm()
    if form.validate_on_submit():
        # create order
        order = Order(customer_name=form.name.data, address=form.address.data, email=form.email.data, total=total)
        db.session.add(order)
        db.session.commit()
        # create order items
        for it in items:
            oi = OrderItem(order_id=order.id, product_id=it['product'].id, qty=it['qty'], price=it['product'].price)
            db.session.add(oi)
        db.session.commit()
        clear_cart()
        flash('Buyurtmangiz qabul qilindi. Rahmat!', 'success')
        return redirect(url_for('home'))
    return render_template('checkout.html', form=form, items=items, total=total)

@app.errorhandler(404)
def not_found(e):
    return render_template('404.html'), 404

# API endpoint (optional) - return products JSON
@app.route('/api/products')
def api_products():
    products = Product.query.all()
    data = [{'id': p.id, 'name': p.name, 'price': p.price, 'stock': p.stock} for p in products]
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
