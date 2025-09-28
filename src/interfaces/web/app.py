import os
from flask import Flask, render_template
from .routes.game_routes import game_routes
from .routes.api_routes import api_routes

app = Flask(__name__)
# Use environment variable for security, fallback only for development
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "dev-only-change-in-production")

# Register blueprints for routes
app.register_blueprint(game_routes, url_prefix="/game")
app.register_blueprint(api_routes, url_prefix="/api")


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/local")
def local_game():
    return render_template("game.html", mode="local")


@app.route("/multiplayer")
def multiplayer_game():
    return render_template("game.html", mode="multiplayer")


def run():
    """Function to run the web app (used by setup.py entry point)"""
    debug_mode = os.getenv('FLASK_DEBUG', 'False').lower() in ['true', '1']
    host = os.getenv('FLASK_HOST', '127.0.0.1')
    port = int(os.getenv('FLASK_PORT', '5000'))
    app.run(debug=debug_mode, host=host, port=port)


if __name__ == "__main__":
    debug_mode = os.getenv('FLASK_DEBUG', 'False').lower() in ['true', '1']
    host = os.getenv('FLASK_HOST', '127.0.0.1')
    port = int(os.getenv('FLASK_PORT', '5000'))
    app.run(debug=debug_mode, host=host, port=port)
