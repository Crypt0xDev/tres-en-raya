from flask import Flask, render_template
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from routes.game_routes import game_routes
from routes.api_routes import api_routes

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
    app.run(debug=True)


if __name__ == "__main__":
    app.run(debug=True)
