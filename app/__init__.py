from flask import Flask
from flask_moment import Moment
from config import config
from livereload import Server
from flask_sqlalchemy import SQLAlchemy
from db_init import *

moment = Moment()
db = SQLAlchemy()


def create_app(config_name):
    app = Flask(__name__)

    # CONFIG
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    # DATABASE
    db.init_app(app)

    # Create tables
    with app.app_context():
        db.create_all()
    # Add calcs, levels etc.
    insert_db_stuff()

    # BLUEPRINTS
    from .main import main as main_blueprint

    app.register_blueprint(main_blueprint)

    # LIVERELOAD
    if app.config["ENV"] == "development":
        server = Server(app)
        server.watch("**/*.*")
        server.serve(host="0.0.0.0", port=5000)

    return app
