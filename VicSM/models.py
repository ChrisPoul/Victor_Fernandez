import click
import os
import glob
from datetime import datetime
from flask import current_app
from flask.cli import with_appcontext
from sqlalchemy import (
    Column, Integer, String, Text, Float, PickleType,
    DateTime, ForeignKey
)
from VicSM import db


class Product(db.Model):
    grupo = Column(String(100), nullable=False)
    serie = Column(String(100), nullable=False)
    codigo = Column(String(100), primary_key=True)
    nombre = Column(String(100), nullable=False, unique=True)
    descripcion = Column(Text, nullable=False)
    marca = Column(String(100), nullable=False)
    imagen = Column(String(100), nullable=False, default="default.png")
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
    recibos = db.relationship(
        'Receipt', backref='author', lazy=True,
        cascade='all, delete-orphan'
    )

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
    db.drop_all()
    db.create_all()

    all_images = get_all_images(current_app)
    for image in all_images:
        os.remove(image)


@click.command('init-db')
@with_appcontext
def init_db_command():
    init_db()
    click.echo('Initialized the database')


def add_item(item):
    db.session.add(item)
    db.session.commit()


def get_all_images(app):
    images_path = os.path.join(app.root_path, "static/images")
    all_images_path = os.path.join(images_path, "*")
    all_images = glob.glob(all_images_path)

    return all_images


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
