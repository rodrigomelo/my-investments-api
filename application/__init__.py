from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()

def create_app():
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object('config.Config')
    db.init_app(app)

    migrate = Migrate(app, db)
    migrate.init_app(app, db)

    with app.app_context():
        from . import routes
        db.create_all()

        return app