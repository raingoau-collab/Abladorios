from flask import Flask, send_from_directory
from app.routes import bp as routes_bp
from pathlib import Path

def create_app():
    app = Flask(__name__)
    app.register_blueprint(routes_bp)

    @app.route("/")
    def index():
        static_dir = Path(__file__).parent / "static"
        return send_from_directory(static_dir, "index.html")

    return app
