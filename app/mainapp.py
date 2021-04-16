

from flask import Flask, render_template, redirect, flash

from application import view
from application.extensions import db, migrate
import os


def create_app(config_object="application.settings"):
    

    app = Flask(__name__.split(".")[0])
    app.config.from_object(config_object)
    register_extensions(app)
    register_blueprints(app)

    return app


def register_extensions(app):
   
    db.init_app(app)
    migrate.init_app(app, db)
    return None


def register_blueprints(app):
    
    app.register_blueprint(view.blueprint)
    return None
