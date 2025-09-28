import os

from flask import Flask, render_template
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

from .routes.api_routes import api_routes
from .routes.game_routes import game_routes

app = Flask(__name__)
# Use environment variable for security, fallback only for development
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "dev-only-change-in-production")

# Configure rate limiting
limiter = Limiter(
    key_func=get_remote_address,
    app=app,
    default_limits=["1000 per day", "200 per hour"],
    storage_uri="memory://",
)

# Register blueprints for routes
app.register_blueprint(game_routes, url_prefix="/game")
app.register_blueprint(api_routes, url_prefix="/api")


@app.route("/")
@limiter.limit("30 per minute")
def index():
    return render_template("index.html")


@app.route("/local")
@limiter.limit("20 per minute")
def local_game():
    return render_template("game.html", mode="local")


@app.route("/multiplayer")
@limiter.limit("10 per minute")
def multiplayer_game():
    return render_template("game.html", mode="multiplayer")


def run():
    """Function to run the web app (used by setup.py entry point)"""
    debug_mode = os.getenv("FLASK_DEBUG", "False").lower() in ["true", "1"]
    host = os.getenv("FLASK_HOST", "127.0.0.1")
    port = int(os.getenv("FLASK_PORT", "5000"))
    app.run(debug=debug_mode, host=host, port=port)


if __name__ == "__main__":
    debug_mode = os.getenv("FLASK_DEBUG", "False").lower() in ["true", "1"]
    host = os.getenv("FLASK_HOST", "127.0.0.1")
    port = int(os.getenv("FLASK_PORT", "5000"))
    app.run(debug=debug_mode, host=host, port=port)
