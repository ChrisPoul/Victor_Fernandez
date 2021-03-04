import click
import os
import glob
import json
from datetime import datetime
from flask import current_app
from flask.cli import with_appcontext
from sqlalchemy import (
    Column, Integer, String, Text, Float, PickleType,
    DateTime, ForeignKey
)
from sqlalchemy.exc import IntegrityError
from VicSM import db


class Product(db.Model):
    grupo = Column(String(100), nullable=False)
    serie = Column(String(100), nullable=False)
    codigo = Column(String(100), primary_key=True)
    nombre = Column(String(100), nullable=False, unique=True)
    descripcion = Column(Text, nullable=False)
    marca = Column(String(100), nullable=False)
    imagen = Column(String(100), nullable=False,
                    default="default.png", unique=True)
    mi_precio = Column(Integer, nullable=False, default=0)
    precio_venta = Column(Integer, nullable=False, default=0)
    inventario = Column(Integer, nullable=False, default=0)
    inv_ref = Column(Integer, nullable=False, default=0)
    unidades_vendidas = Column(Integer, nullable=False, default=0)

    def __repr__(self):
        return self.__dict__


class Client(db.Model):
    id = Column(Integer, primary_key=True)
    nombre = Column(String(100), nullable=False, unique=True)
    direccion = Column(String(200), nullable=False)
    tel = Column(String(20), nullable=False, unique=True)
    proyecto = Column(String(100), nullable=False)
    descripcion = Column(Text, nullable=False)
    cotizacion = Column(String(100), nullable=False)
    cambio = Column(Integer, nullable=False, default=0)
    recibos = db.relationship(
        'Receipt', backref='author', lazy=True,
        cascade='all, delete-orphan'
    )
    total = Column(Integer, nullable=False, default=0)

    def __repr__(self):
        return self.__dict__


class Receipt(db.Model):
    id = Column(Integer, primary_key=True)
    grupo = Column(String(100), nullable=True, default=None)
    cambio = Column(Float, nullable=True, default=None)
    totales = Column(PickleType, nullable=False, default={})
    total = Column(Float, nullable=False, default=0)
    cantidades = Column(PickleType, nullable=False, default={})
    cant_ref = Column(PickleType, nullable=False, default={})
    fecha = Column(DateTime, nullable=False, default=datetime.now)
    client_id = Column(Integer, ForeignKey('client.id'), nullable=False)

    def __repr__(self):
        return self.__dict__


def init_db():
    # Client.__table__.drop(db.engine)
    # Receipt.__table__.drop(db.engine)
    # Product.__table__.drop(db.engine)
    # db.drop_all()
    db.create_all()

    references = get_references()
    references['ventas'] = [0]
    references['utilidades'] = [0]
    save_references(references)


@click.command('init-db')
@with_appcontext
def init_db_command():
    init_db()
    click.echo('Initialized the database')


def get_references():
    references_path = os.path.join(current_app.static_folder, 'references.json')
    with open(references_path, 'r') as references_file:
        references = json.load(references_file)

    return references


def save_references(references):
    references_path = os.path.join(current_app.static_folder, 'references.json')
    json_references = json.dumps(references, indent=4)
    with open(references_path, "w") as references_file:
        references_file.write(json_references)


def add_item(item):
    db.session.add(item)
    error = None
    try:
        db.session.commit()
    except IntegrityError:
        error = "Error, uno de los valores que introdujo ya se encuentra en uso"

    return error


def get_all_images(app):
    images_path = os.path.join(app.root_path, "static/images")
    all_images_path = os.path.join(images_path, "*")
    all_images = glob.glob(all_images_path)

    return all_images


def save_image(image_file):
    if image_file:
        images_path = os.path.join(current_app.root_path, "static/images")
        image_path = os.path.join(images_path, image_file.filename)
        image_file.save(image_path)


def remove_image(image_name):
    if image_name:
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


def obj_as_dict(obj_tuple):
    obj_dict = {}
    for key in obj_tuple:
        obj_dict[key] = obj_tuple[key]

    return obj_dict
