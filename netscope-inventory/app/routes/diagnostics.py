from flask import Blueprint, render_template, jsonify
import time
from datetime import datetime
from app import db
from sqlalchemy import text
from app.services.network import get_server_identity
from app.diagnostics.network_info import get_network_info
from flask import request

bp = Blueprint('diagnostics', __name__)

@bp.route('/diagnostics')
def dashboard():
    info = get_network_info()
    
    # Test DB Connection for dashboard
    db_status = "Unknown"
    try:
        db.session.execute(text('SELECT 1'))
        db_status = "Connected"
    except Exception as e:
        db_status = f"Failed: {str(e)}"
        
    info['db_status'] = db_status
    return render_template('diagnostics/dashboard.html', info=info)

@bp.route('/health')
def health():
    try:
        db.session.execute(text('SELECT 1'))
        db_state = "up"
    except Exception:
        db_state = "down"
        
    status = "healthy" if db_state == "up" else "unhealthy"
    status_code = 200 if status == "healthy" else 503
    
    return jsonify({
        "status": status,
        "application": "up",
        "database": db_state,
        "timestamp": datetime.utcnow().isoformat(),
        "server": get_server_identity()
    }), status_code

@bp.route('/dbtest')
def dbtest():
    start_time = time.time()
    try:
        db.session.execute(text('SELECT 1'))
        latency = (time.time() - start_time) * 1000
        engine_name = db.engine.name
        return jsonify({
            "database": "connected",
            "server": engine_name,
            "latency_ms": round(latency, 2)
        })
    except Exception as e:
        return jsonify({
            "database": "failed",
            "error": str(e)
        }), 500

@bp.route('/network')
def network():
    identity = get_server_identity()
    identity['current_time'] = datetime.utcnow().isoformat()
    return jsonify(identity)

@bp.route('/headers')
def headers():
    return jsonify(dict(request.headers))

@bp.route('/clientip')
def clientip():
    info = get_network_info()
    return jsonify(info['client'])

@bp.route('/ssltest')
def ssltest():
    info = get_network_info()
    return jsonify(info['ssl'])

@bp.route('/slow')
def slow():
    time.sleep(10)
    return jsonify({
        "status": "success",
        "message": "Response delayed by 10 seconds",
        "server": get_server_identity()
    })

@bp.route('/error')
def error():
    # Intentionally raise an error
    raise Exception("This is an intentional error for testing 500 responses and WAF rules.")
