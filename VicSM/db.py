import sqlite3
import json
import click
import os
import glob
import datetime
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

    receipts = {}
    save_receipts(receipts)
    recent = {}

    images_path = os.path.join(current_app.root_path, "static/images")
    all_images_path = os.path.join(images_path, "*")
    all_images = glob.glob(all_images_path)
    for image in all_images:
        os.remove(image)


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


def get_client_receipts(client_id):
    receipts = get_receipts()
    client_id = str(client_id)
    client_receipts = receipts[client_id]

    return client_receipts


def get_receipt(client_id, receipt_id):
    client_id = str(client_id)
    receipt_id = str(receipt_id)
    try:
        client_receipts = get_client_receipts(client_id)
        receipt = client_receipts[receipt_id]
    except KeyError:
        receipt = {
        "grupo": None,
        "cambio": None,
        "totals": {},
        "total": 0,
        "cantidades": {},
        "fecha": format_date(datetime.date.today())
        }

    return receipt


def save_receipts(receipts):
    receipts_path = os.path.join(current_app.instance_path, "receipts.json")
    with open(receipts_path, "w+") as receipts_file:
        json_receipts = json.dumps(receipts, indent=2)
        receipts_file.write(json_receipts)


def save_receipt(client_id, receipt_id, receipt):
    receipts = get_receipts()
    client_id = str(client_id)
    try:
        client_receipts = receipts[client_id]
    except KeyError:
        client_receipts = {"numero_de_recibos": 0}
    
    if receipt_id == 0:
        receipt_id = client_receipts["numero_de_recibos"] + 1
        client_receipts["numero_de_recibos"] += 1

    client_receipts[str(receipt_id)] = receipt
    receipts[client_id] = client_receipts
    save_receipts(receipts)


def get_recent():
    recent_path = os.path.join(current_app.instance_path, "recent.json")
    with open(recent_path) as recent_file:
        recent = json.load(recent_file)

    return recent


def save_recent(recent):
    recent_path = os.path.join(current_app.instance_path, "recent.json")
    with open(recent_path, "w+") as recent_file:
        json_recent = json.dumps(recent, indent=2)
        recent_file.write(json_recent)



days = {
    "0": "Lunes", "1": "Martes",
    "2": "Miercoles", "3": "Jueves",
    "4": "Viernes", "5": "Sábado",
    "6": "Domingo"
}
months = {
    "01": "Enero", "02": "Febrero",
    "03": "Marzo", "04": "Abril",
    "05": "Mayo", "06": "Junio",
    "07": "Julio", "08": "Agosto",
    "09": "Septiembre", "10": "Octubre",
    "11": "Noviembre", "12": "Diciembre"
}


def format_date(date):
    str_date = date.strftime("%d/%m/%Y")
    date_parts = str_date.split("/")

    week_day = date.weekday()
    day = days[str(week_day)]
    day_num = date_parts[0]
    
    month = date_parts[1]
    month = months[month]
    year = date_parts[2]

    return f"{day} {day_num} de {month} del {year}"

