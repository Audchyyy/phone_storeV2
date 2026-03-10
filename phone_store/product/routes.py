import os, secrets
from PIL import Image
from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from phone_store.product import product_bp
from phone_store.extensions import db
from phone_store.models import Product

def save_product_image(file):
    random_hex = secrets.token_hex(8)
    _, ext = os.path.splitext(file.filename)
    filename = random_hex + ext
    path = os.path.join(product_bp.root_path, '../static/img', filename)
    img = Image.open(file)
    img.thumbnail((800, 800))
    img.save(path)
    return filename

def save_product_model(file):
    random_hex = secrets.token_hex(8)
    _, ext = os.path.splitext(file.filename)
    filename = random_hex + ext
    path = os.path.join(product_bp.root_path, '../static/models', filename)
    file.save(path)
    return filename

@product_bp.route('/mac')
def mac():
    products = Product.query.filter_by(category='mac').all()
    return render_template('product/mac.html', products=products)

@product_bp.route('/mac/<int:id>')
def mac_detail(id):
    product = Product.query.get_or_404(id)
    return render_template('product/mac_detail.html', product=product)

@product_bp.route('/ipad')
def ipad():
    products = Product.query.filter_by(category='ipad').all()
    return render_template('product/ipad.html', products=products)

@product_bp.route('/ipad/<int:id>')
def ipad_detail(id):
    product = Product.query.get_or_404(id)
    return render_template('product/ipad_detail.html', product=product)

@product_bp.route('/iphone')
def iphone():
    products = Product.query.filter_by(category='iphone').all()
    return render_template('product/iphone.html', products=products)

@product_bp.route('/iphone/<int:id>')
def iphone_detail(id):
    product = Product.query.get_or_404(id)
    return render_template('product/iphone_detail.html', product=product)

@product_bp.route('/watch')
def watch():
    products = Product.query.filter_by(category='watch').all()
    return render_template('product/watch.html', products=products)

@product_bp.route('/watch/<int:id>')
def watch_detail(id):
    product = Product.query.get_or_404(id)
    return render_template('product/watch_detail.html', product=product)

@product_bp.route('/airpods')
def airpods():
    products = Product.query.filter_by(category='airpods').all()
    return render_template('product/airpods.html', products=products)

@product_bp.route('/airpods/<int:id>')
def airpods_detail(id):
    product = Product.query.get_or_404(id)
    return render_template('product/airpods_detail.html', product=product)

@product_bp.route('/products')
@login_required
def products():
    my_products = Product.query.filter_by(user_id=current_user.id).all()
    return render_template('product/products.html', products=my_products)

@product_bp.route('/product/add', methods=['GET', 'POST'])
@login_required
def add():
    if request.method == 'POST':
        image_url = None
        if 'image' in request.files and request.files['image'].filename != '':
            image_url = '/static/img/' + save_product_image(request.files['image'])
        model_url = None
        if 'model' in request.files and request.files['model'].filename != '':
            model_url = '/static/models/' + save_product_model(request.files['model'])
        product = Product(
            name        = request.form.get('name'),
            subtitle    = request.form.get('subtitle'),
            description = request.form.get('description'),
            price       = float(request.form.get('price', 0)),
            category    = request.form.get('category', 'mac'),
            image_url   = image_url,
            model_url   = model_url,
            badge       = request.form.get('badge'),
            user_id     = current_user.id
        )
        db.session.add(product)
        db.session.commit()
        flash(f'เพิ่ม "{product.name}" สำเร็จ', 'success')
        return redirect(url_for('product.mac'))
    return render_template('product/product_add.html')

@product_bp.route('/product/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    product = Product.query.get_or_404(id)
    if request.method == 'POST':
        product.name        = request.form.get('name')
        product.subtitle    = request.form.get('subtitle')
        product.description = request.form.get('description')
        product.price       = float(request.form.get('price', 0))
        product.badge       = request.form.get('badge')
        if 'image' in request.files and request.files['image'].filename != '':
            product.image_url = '/static/img/' + save_product_image(request.files['image'])
        if 'model' in request.files and request.files['model'].filename != '':
            product.model_url = '/static/models/' + save_product_model(request.files['model'])
        db.session.commit()
        flash(f'แก้ไข "{product.name}" สำเร็จ', 'success')
        return redirect(url_for('product.products'))
    return render_template('product/product_edit.html', product=product)

@product_bp.route('/product/delete/<int:id>', methods=['POST'])
@login_required
def delete(id):
    product = Product.query.get_or_404(id)
    db.session.delete(product)
    db.session.commit()
    flash(f'ลบ "{product.name}" แล้ว', 'success')
    return redirect(url_for('product.products'))

@product_bp.route('/search')
def search():
    q = request.args.get('q', '')
    results = Product.query.filter(Product.name.ilike(f'%{q}%')).all()
    return render_template('product/search.html', products=results, query=q)