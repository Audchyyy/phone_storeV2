from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import current_user, login_user, logout_user, login_required
from phone_store.models import User, Order
from phone_store.extensions import db, bcrypt
from phone_store.forms import UpdateAccountForm, LoginForm, RegisterForm, ChangePasswordForm
import os, secrets
from PIL import Image

user_bp = Blueprint('user', __name__, template_folder='templates', static_folder='static')

@user_bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        hash_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hash_password)
        db.session.add(user)
        db.session.commit()
        flash('สมัครสมาชิกสำเร็จ!', 'success')
        return redirect(url_for('user.login'))
    return render_template('user/register.html', title='Register', form=form)

@user_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.scalar(db.select(User).where(User.email == form.email.data))
        if not user:
            user = db.session.scalar(db.select(User).where(User.username == form.email.data))
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user=user, remember=form.remember.data)
            return redirect(url_for('core.index'))
        flash('อีเมล/ยูสเซอร์เนมหรือรหัสผ่านไม่ถูกต้อง', 'danger')
    return render_template('user/login.html', title='Sign In', form=form)

@user_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('user.login'))

def save_avatar(form_avatar):
    random_hex = secrets.token_hex(8)
    _, ext = os.path.splitext(form_avatar.filename)
    avatar_fn = random_hex + ext
    avatar_path = os.path.join(user_bp.root_path, 'static/img', avatar_fn)
    img = Image.open(form_avatar)
    img.thumbnail((256, 256))
    img.save(avatar_path)
    return avatar_fn

@user_bp.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if request.method == 'GET':
        form.username.data = current_user.username
        form.email.data    = current_user.email
        form.fullname.data = current_user.fullname
    elif form.validate_on_submit():
        if form.avatar.data:
            current_user.avatar = save_avatar(form.avatar.data)
        current_user.fullname = form.fullname.data
        db.session.commit()
        flash('อัปเดตบัญชีสำเร็จ!', 'success')
        return redirect(url_for('user.account'))
    return render_template('user/account.html', title='Account', form=form,
                           avatar_pic=current_user.avatar)


@user_bp.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if bcrypt.check_password_hash(current_user.password, form.current_password.data):
            current_user.password = bcrypt.generate_password_hash(form.new_password.data).decode('utf-8')
            db.session.commit()
            flash('เปลี่ยนรหัสผ่านสำเร็จ!', 'success')
            return redirect(url_for('user.account'))
        flash('รหัสผ่านปัจจุบันไม่ถูกต้อง', 'danger')
    return render_template('user/change_password.html', title='Change Password', form=form)

@user_bp.route('/orders')
@login_required
def orders():
    order_list = db.session.scalars(
        db.select(Order).where(Order.user_id == current_user.id).order_by(Order.ordered_at.desc())
    ).all()
    total_spent = sum(o.total for o in order_list)
    total_items = sum(sum(i.quantity for i in o.items) for o in order_list)
    return render_template('user/orders.html', title='ประวัติการสั่งซื้อ',
                           orders=order_list, total_spent=total_spent, total_items=total_items)