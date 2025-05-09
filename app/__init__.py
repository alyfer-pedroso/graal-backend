from flask import Flask

from .routes.cargo_route import cargo_bp

def create_app():
    app = Flask(__name__)
    app.config['DEBUG'] = True

    app.register_blueprint(cargo_bp)

    return app
