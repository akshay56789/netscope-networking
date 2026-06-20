import socket
import os
import platform
import flask

def get_server_identity():
    """
    Returns server identity information including hostname, private IP, and OS details.
    """
    hostname = socket.gethostname()
    try:
        # Get primary private IP
        ip_address = socket.gethostbyname(hostname)
    except Exception:
        ip_address = '127.0.0.1'
        
    return {
        "hostname": hostname,
        "ip": ip_address,
        "os": platform.system(),
        "os_release": platform.release(),
        "flask_version": flask.__version__
    }
