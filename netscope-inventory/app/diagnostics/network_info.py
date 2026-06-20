import time
from flask import request
from app.services.network import get_server_identity

def get_network_info():
    """Gather comprehensive network and server diagnostics"""
    identity = get_server_identity()
    
    # Process headers
    headers_dict = dict(request.headers)
    
    # IP Resolution
    real_client_ip = request.headers.get('X-Real-IP', request.remote_addr)
    forwarded_for = request.headers.get('X-Forwarded-For', '')
    
    # SSL/Scheme
    scheme = request.headers.get('X-Forwarded-Proto', request.scheme)
    is_secure = scheme == 'https'
    
    return {
        "server": identity,
        "client": {
            "remote_addr": request.remote_addr,
            "x_forwarded_for": forwarded_for,
            "real_client_ip": real_client_ip
        },
        "ssl": {
            "scheme": scheme,
            "secure": is_secure
        },
        "headers": headers_dict
    }
