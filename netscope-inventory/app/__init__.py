import os
import logging
from flask import Flask, request, g
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from flask_wtf.csrf import CSRFProtect
from logging.handlers import RotatingFileHandler
from datetime import datetime

# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()
cors = CORS()
csrf = CSRFProtect()

def create_app(config_class='config.Config'):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Trust proxy headers when deployed behind a reverse proxy/load balancer
    from werkzeug.middleware.proxy_fix import ProxyFix
    app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)

    # Initialize Flask extensions
    db.init_app(app)
    migrate.init_app(app, db)
    cors.init_app(app)
    # Enable CSRF protection, but we might want to exclude API routes
    csrf.init_app(app)
    csrf.exempt('app.routes.api') # Exempt API routes from CSRF
    
    # Configure Logging
    configure_logging(app)

    # Register blueprints
    from app.routes.main import bp as main_bp
    app.register_blueprint(main_bp)

    from app.routes.products import bp as products_bp
    app.register_blueprint(products_bp, url_prefix='/products')

    from app.routes.diagnostics import bp as diagnostics_bp
    app.register_blueprint(diagnostics_bp)

    from app.routes.api import bp as api_bp
    app.register_blueprint(api_bp, url_prefix='/api')
    
    # Request logging middleware
    @app.before_request
    def before_request():
        g.start_time = datetime.utcnow()

    @app.after_request
    def after_request(response):
        if not request.path.startswith('/static'):
            duration = (datetime.utcnow() - getattr(g, 'start_time', datetime.utcnow())).total_seconds() * 1000
            
            # Use real client IP if forwarded, else fallback
            client_ip = request.headers.get('X-Forwarded-For', request.remote_addr)
            if client_ip and ',' in client_ip:
                client_ip = client_ip.split(',')[0].strip()
                
            app.logger.info(
                f"{client_ip} - {request.method} {request.url} - {response.status_code} - {duration:.2f}ms"
            )
        return response

    return app

def configure_logging(app):
    if not os.path.exists('logs'):
        os.mkdir('logs')
        
    file_handler = RotatingFileHandler('logs/app.log', maxBytes=10240000, backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    ))
    file_handler.setLevel(logging.INFO)
    
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)
    app.logger.info('NetScope Inventory startup')
