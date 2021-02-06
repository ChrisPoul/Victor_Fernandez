import sqlite3
import json
import click
import os
from flask import current_app, g
from flask.cli import with_appcontext


def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()


def init_db():
    db = get_db()

    with current_app.open_resource('schema.sql') as file:
        script = file.read().decode('utf8')
        db.executescript(script)

    receipts = get_receipts()
    receipts = {}
    save_receipts(receipts)

    images_path = os.path.join(current_app.root_path, "static/images")
    all_images = os.path.join(images_path, "*")
    os.system(f'rm {all_images}')


@click.command('init-db')
@with_appcontext
def init_db_command():
    init_db()
    click.echo('Initialized the database')


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)


def get_receipts():
    receipts_path = os.path.join(current_app.instance_path, "receipts.json")
    with open(receipts_path) as receipts_file:
        receipts = json.load(receipts_file)

    return receipts


def save_receipts(receipts):
    json_receipts = json.dumps(receipts)
    receipts_path = os.path.join(current_app.instance_path, "receipts.json")

    with open(receipts_path, "w+") as receipts_file:
        receipts_file.write(json_receipts)