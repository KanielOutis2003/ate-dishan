from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bootstrap import Bootstrap4  # Use Bootstrap4 instead of Bootstrap

# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()
bootstrap = Bootstrap4()  # Correct usage for Bootstrap-Flask

def create_app():
    app = Flask(__name__)
    
    # Configuration settings
    app.config['SECRET_KEY'] = 'your-secret-key-here'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///school_system.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize extensions with app
    db.init_app(app)
    migrate.init_app(app, db)
    bootstrap.init_app(app)

    # Import routes after db initialization to avoid circular imports
    from app.routes import bp
    app.register_blueprint(bp)

    return app
