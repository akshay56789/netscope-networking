from flask import Blueprint, jsonify
from app.services.network import get_server_identity

bp = Blueprint('api', __name__)

@bp.route('/products')
def api_products():
    return jsonify({
        "message": "Products API Backend",
        "data": [
            {"id": 1, "name": "Enterprise Switch"},
            {"id": 2, "name": "Core Router"}
        ],
        "server": get_server_identity()
    })

@bp.route('/users')
def api_users():
    return jsonify({
        "message": "Users API Backend",
        "data": [
            {"id": 1, "name": "Admin"},
            {"id": 2, "name": "Network Engineer"}
        ],
        "server": get_server_identity()
    })

@bp.route('/orders')
def api_orders():
    return jsonify({
        "message": "Orders API Backend",
        "data": [
            {"id": 1001, "status": "Shipped"},
            {"id": 1002, "status": "Processing"}
        ],
        "server": get_server_identity()
    })
