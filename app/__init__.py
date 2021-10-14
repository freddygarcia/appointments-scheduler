from flask import Flask
from .routes import appointment

app = Flask(__name__)

app.register_blueprint(appointment)