from flask import Flask, jsonify
from flask_cors import CORS
from flask_mail import Mail
import os
from dotenv import load_dotenv
from app.database import test_connection

load_dotenv()

mail = Mail()

def create_app():
    app = Flask(__name__)
    
    # Test MongoDB connection
    if not test_connection():
        print("WARNING: MongoDB connection failed. Application may not work correctly.")
    
    # Configure app
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "your-secret-key-here")
    
    # Email configuration
    app.config['MAIL_SERVER'] = os.getenv("MAIL_SERVER", "smtp.gmail.com")
    app.config['MAIL_PORT'] = int(os.getenv("MAIL_PORT", "587"))
    app.config['MAIL_USE_TLS'] = os.getenv("MAIL_USE_TLS", "True") == "True"
    app.config['MAIL_USERNAME'] = os.getenv("MAIL_USERNAME")
    app.config['MAIL_PASSWORD'] = os.getenv("MAIL_PASSWORD")
    app.config['MAIL_DEFAULT_SENDER'] = os.getenv("MAIL_DEFAULT_SENDER")
    
    # Initialize extensions
    mail.init_app(app)
    CORS(app)
    
    # Register blueprints
    from app.routes.examiner_routes import examiner_bp
    from app.routes.venue_routes import venue_bp
    from app.routes.presentation_routes import presentation_bp
    
    app.register_blueprint(examiner_bp, url_prefix='/api/examiners')
    app.register_blueprint(venue_bp, url_prefix='/api/venues')
    app.register_blueprint(presentation_bp, url_prefix='/api/presentations')
    
    # Add a custom JSON encoder for ObjectId
    from flask.json import JSONEncoder
    from bson import ObjectId
    
    class CustomJSONEncoder(JSONEncoder):
        def default(self, obj):
            if isinstance(obj, ObjectId):
                return str(obj)
            return super().default(obj)
    
    app.json_encoder = CustomJSONEncoder
    
    return app