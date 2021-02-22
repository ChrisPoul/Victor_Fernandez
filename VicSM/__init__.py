import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{app.instance_path}/VicSM.sqlite"

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    db.init_app(app)

    from .models import init_db_command
    app.cli.add_command(init_db_command)

    from . import main_page
    app.register_blueprint(main_page.bp)

    from . import inventory
    app.register_blueprint(inventory.bp)

    from . import receipt
    app.register_blueprint(receipt.bp)

    from . import client
    app.register_blueprint(client.bp)

    return app
