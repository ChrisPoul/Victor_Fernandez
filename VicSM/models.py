import json
import click
import os
import glob
import datetime
from flask import current_app
from flask.cli import with_appcontext
from sqlalchemy import (
    Column, Integer, String, Text
)
from VicSM import db


def init_db():
    db.drop_all()
    db.create_all()

    receipts = {}
    save_receipts(receipts)

    all_images = get_all_images(current_app)
    for image in all_images:
        os.remove(image)


@click.command('init-db')
@with_appcontext
def init_db_command():
    init_db()
    click.echo('Initialized the database')


def save_item(item):
    db.session.add(item)
    db.session.commit()


class Product(db.Model):
    grupo = Column(String(100), nullable=False)
    serie = Column(String(100), nullable=False)
    codigo = Column(String(100), primary_key=True)
    nombre = Column(String(100), nullable=False, unique=True)
    descripcion = Column(Text, nullable=False)
    marca = Column(String(100), nullable=False)
    imagen = Column(String(100), nullable=False, default="default.jpg")
    mi_precio = Column(Integer, nullable=False, default=0)
    precio_venta = Column(Integer, nullable=False, default=0)
    inventario = Column(Integer, nullable=False, default=0)

    def __repr__(self):
        return self.__dict__


class Client(db.Model):
    id = Column(Integer, primary_key=True)
    nombre = Column(String(100), nullable=False)
    direccion = Column(String(200), nullable=False)
    tel = Column(String(20), nullable=False)
    proyecto = Column(String(100), nullable=False)
    descripcion = Column(Text, nullable=False)
    cotizacion = Column(String(100), nullable=False)
    cambio = Column(Integer, nullable=False, default=0)

    def __repr__(self):
        return self.__dict__


def get_all_images(app):
    images_path = os.path.join(app.root_path, "static/images")
    all_images_path = os.path.join(images_path, "*")
    all_images = glob.glob(all_images_path)

    return all_images


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
        json_receipts = json.dumps(receipts, indent=4)
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


def save_image(image_file):
    images_path = os.path.join(current_app.root_path, "static/images")
    image_path = os.path.join(images_path, image_file.filename)
    image_file.save(image_path)


def remove_image(image_name):
    try:
        images_path = os.path.join(current_app.root_path, "static/images")
        image_path = os.path.join(images_path, image_name)
        os.remove(image_path)
    except FileNotFoundError:
        pass


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
