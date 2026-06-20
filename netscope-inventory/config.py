import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-fallback-secret-key'
    
    # Check if a direct URI is provided (like sqlite:///...)
    db_uri = os.environ.get('SQLALCHEMY_DATABASE_URI')
    
    if not db_uri:
        # Construct MySQL URI if individual variables are provided
        db_user = os.environ.get('DB_USER')
        db_pass = os.environ.get('DB_PASSWORD')
        db_host = os.environ.get('DB_HOST')
        db_port = os.environ.get('DB_PORT', '3306')
        db_name = os.environ.get('DB_NAME')
        
        if all([db_user, db_pass, db_host, db_name]):
            db_uri = f"mysql+pymysql://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}"
        else:
            # Fallback to SQLite for local development
            db_uri = 'sqlite:///' + os.path.join(basedir, 'netscope.db')
            
    SQLALCHEMY_DATABASE_URI = db_uri
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Used for reverse proxy configurations
    USE_X_SENDFILE = True
