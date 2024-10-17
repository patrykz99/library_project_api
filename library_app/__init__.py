from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


db = SQLAlchemy()
migrate = Migrate()


def build_app(config_cls = Config):
    #factory pattern
    app = Flask(__name__)
    app.config.from_object(config_cls)    
    
    db.init_app(app)
    migrate.init_app(app,db)
    
    #import blueprints
    from library_app.authors import authors_blueprint
    from library_app.books import books_blueprint
    from library_app.commands import db_commands_blueprint
    from library_app.errors import errors_blueprint
    app.register_blueprint(authors_blueprint,url_prefix='/api/ver1')
    app.register_blueprint(books_blueprint,url_prefix='/api/ver1')
    app.register_blueprint(db_commands_blueprint)
    app.register_blueprint(errors_blueprint)
    
    return app
    