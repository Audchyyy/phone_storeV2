from flask import Blueprint
cart_bp = Blueprint('cart', __name__, template_folder='templates')
from phone_store.cart import routes
