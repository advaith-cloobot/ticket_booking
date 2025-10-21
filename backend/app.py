from flask import Flask, jsonify
from flask_cors import CORS
from flask_migrate import Migrate
from flask_mail import Mail
from flask_jwt_extended import JWTManager
from config import Config
from models import db, User
from api.auth_routes import auth_bp
from api.movie_routes import movie_bp
from api.booking_routes import booking_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Initialize extensions
    db.init_app(app)
    migrate = Migrate(app, db)
    CORS(app)
    mail = Mail(app)
    jwt = JWTManager(app)
    
    # Configure JWT to ensure string identities
    @jwt.user_identity_loader
    def user_identity_lookup(user):
        return str(user)
    
    @jwt.user_lookup_loader
    def user_lookup_callback(_jwt_header, jwt_data):
        identity = jwt_data["sub"]
        return User.query.filter_by(id=int(identity)).one_or_none()
    
    # Register blueprints
    app.register_blueprint(auth_bp, url_prefix='/api')
    app.register_blueprint(movie_bp, url_prefix='/api')
    app.register_blueprint(booking_bp, url_prefix='/api')
    
    @app.route('/')
    def index():
        return {'message': 'Movie Ticket Booking API'}
    
    return app

if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5000)
