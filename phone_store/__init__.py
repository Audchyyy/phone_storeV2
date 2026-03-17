from flask import Flask
from phone_store.extensions import db, bcrypt, login_manager
from phone_store.core.routes import core_bp
from phone_store.user.routes import user_bp
from phone_store.cart.routes import cart_bp
import os

def create_app():
    app = Flask(__name__, template_folder='templates', static_folder='static')

    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URI')
    app.secret_key = os.environ.get('SECRET_KEY', 'dev-secret-key')

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'user.login'
    login_manager.login_message = 'กรุณาเข้าสู่ระบบก่อนเข้าถึงหน้านี้'
    login_manager.login_message_category = 'warning'

    from phone_store.product.routes import product_bp  

    app.register_blueprint(core_bp,    url_prefix='/')
    app.register_blueprint(user_bp,    url_prefix='/user')
    app.register_blueprint(product_bp, url_prefix='/')
    app.register_blueprint(cart_bp,    url_prefix='/cart')

    return app