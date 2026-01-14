from flask import Flask
from flask_cors import CORS
from app.config import Config
from app.routes import blueprints

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    CORS(app)
    
    for blueprint in blueprints:
        app.register_blueprint(blueprint)
        
    @app.route('/health')
    def health():
        return {'status': 'healthy', 'message': 'F1 API is running'}, 200
        
    return app