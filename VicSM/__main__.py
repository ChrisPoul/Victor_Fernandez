import os
from webui import WebUI
from flask import Flask, render_template

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'VicSM.sqlite')
    )

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from . import db
    db.init_app(app)

    from . import inventory
    app.register_blueprint(inventory.bp)

    from . import receipt
    app.register_blueprint(receipt.bp)

    from . import client
    app.register_blueprint(client.bp)

    return app


if __name__ == "__main__":
    app = create_app()
    ui = WebUI(app, debug=True)
    ui.view.page().profile().clearHttpCache()
    ui.run()