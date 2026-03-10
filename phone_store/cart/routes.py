from flask import render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from phone_store.cart import cart_bp
from phone_store.extensions import db
from phone_store.models import CartItem, Product

@cart_bp.route('/')
@login_required
def index():
    items = CartItem.query.filter_by(user_id=current_user.id).all()
    total = sum(item.subtotal() for item in items)
    return render_template('cart/index.html', title='ตะกร้าสินค้า', items=items, total=total)

@cart_bp.route('/add/<int:product_id>', methods=['POST'])
@login_required
def add(product_id):
    product = Product.query.get_or_404(product_id)
    item = CartItem.query.filter_by(user_id=current_user.id, product_id=product_id).first()
    if item:
        item.quantity += 1
    else:
        item = CartItem(user_id=current_user.id, product_id=product_id, quantity=1)
        db.session.add(item)
    db.session.commit()
    flash(f'เพิ่ม "{product.name}" ลงตะกร้าแล้ว', 'success')
    return redirect(request.referrer or url_for('product.mac'))

@cart_bp.route('/update/<int:item_id>', methods=['POST'])
@login_required
def update(item_id):
    item = CartItem.query.get_or_404(item_id)
    if item.user_id != current_user.id:
        flash('ไม่มีสิทธิ์', 'danger')
        return redirect(url_for('cart.index'))
    qty = int(request.form.get('quantity', 1))
    if qty < 1:
        db.session.delete(item)
    else:
        item.quantity = qty
    db.session.commit()
    return redirect(url_for('cart.index'))

@cart_bp.route('/remove/<int:item_id>', methods=['POST'])
@login_required
def remove(item_id):
    item = CartItem.query.get_or_404(item_id)
    if item.user_id != current_user.id:
        flash('ไม่มีสิทธิ์', 'danger')
        return redirect(url_for('cart.index'))
    db.session.delete(item)
    db.session.commit()
    flash('ลบสินค้าออกจากตะกร้าแล้ว', 'success')
    return redirect(url_for('cart.index'))

@cart_bp.route('/clear', methods=['POST'])
@login_required
def clear():
    CartItem.query.filter_by(user_id=current_user.id).delete()
    db.session.commit()
    flash('ล้างตะกร้าแล้ว', 'success')
    return redirect(url_for('cart.index'))

@cart_bp.route('/checkout', methods=['GET', 'POST'])
@login_required
def checkout():
    items = CartItem.query.filter_by(user_id=current_user.id).all()
    if not items:
        flash('ตะกร้าว่างเปล่า', 'warning')
        return redirect(url_for('cart.index'))
    total = sum(item.subtotal() for item in items)
    if request.method == 'POST':
        CartItem.query.filter_by(user_id=current_user.id).delete()
        db.session.commit()
        flash('สั่งซื้อสำเร็จ! ขอบคุณที่ใช้บริการ 🎉', 'success')
        return redirect(url_for('core.index'))
    return render_template('cart/checkout.html', title='ยืนยันการสั่งซื้อ', items=items, total=total)
