# Import all route blueprints
# from app.routes.meetings import bp as meetings_bp
# from app.routes.sessions import bp as sessions_bp
from app.routes.drivers import bp as drivers_bp

# List of all blueprints to register
blueprints = [
    # meetings_bp,
    # sessions_bp,
    drivers_bp
]