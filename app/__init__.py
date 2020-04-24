from flask import Flask
from config import Config
from flask_bootstrap import Bootstrap
from flask_session import Session
import os

app = Flask(__name__)
app.config.from_object(Config)
Bootstrap(app)
Session(app)

from app import routes