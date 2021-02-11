from flask import (
    Blueprint, g, render_template, request, flash, redirect, url_for, current_app
)
from VicSM.db import get_db
import os

bp = Blueprint('inventory', __name__)

heads = {
    "grupo": "Grupo", "serie": "Serie", "codigo": "Código", "nombre": "Nombre", 
    "descripcion": "Descripción", "marca": "Marca", "imagen": "Imagen", 
    "mi_precio": "Mi Precio", "precio_venta": "Precio Venta", "inventario" : "Inventario"
    }
search_heads = {}
for head in heads:
    if head != "descripcion" and head != "imagen":
        search_heads[head] = heads[head]


def format_price(num):
    num = str(num)
    if "." not in num:
        num += ".00"
    
    num_parts = num.split(".")
    num_int = num_parts[0]
    num_dec = num_parts[1]

    if len(num_dec) == 1:
        num_dec += "0"

    comma_track = 1
    int_with_commas = ""
    for i, num in enumerate(num_int[::-1]):
        int_with_commas += num
        if comma_track == 3 and i != len(num_int)-1:
            int_with_commas += ","
            comma_track = 0

        comma_track += 1

    num_int = int_with_commas[::-1]
    num = f"${num_int}.{num_dec}"

    return num


def add_iva(num):
    num = round(float(num) * 1.16, 2)

    return format_price(num)


def get_products(search_term):
    db = get_db()
    products = None
    for head in search_heads:
            products = db.execute(
                f'SELECT * FROM product WHERE {head} = ?',(search_term,)
            ).fetchall()

            if products:
                return products

    if not products:
        products = db.execute(
            'SELECT * FROM product'
        ).fetchall()

    return products


def get_product(codigo):
    db = get_db()
    product = db.execute(
        'SELECT * FROM product WHERE codigo = ?', (codigo,)
    ).fetchone()

    return product


@bp.route('/inventory', methods=('POST', 'GET'))
def inventory():
    db = get_db()
    search_term = "0"
    if request.method == 'POST':
        search_term = request.form["search_term"]
    
    products = get_products(search_term)

    return render_template('inventory/inventory.html',
        products=products, heads=heads, format_price=format_price
    )


def save_image(current_app, image_file):
    images_path = os.path.join(current_app.root_path, "static/images")
    image_path = os.path.join(images_path, image_file.filename)
    image_file.save(image_path)


@bp.route('/add_product', methods=('GET', 'POST'))
def add_product():
    if request.method == 'POST':
        grupo = request.form["grupo"]
        serie = request.form["serie"]
        codigo = request.form["codigo"]
        nombre = request.form["nombre"]
        descripcion = request.form["descripcion"] 
        marca = request.form["marca"]
        imagen_file = request.files["imagen"]
        imagen = imagen_file.filename
        mi_precio = request.form["mi_precio"]
        precio_venta = request.form["precio_venta"]
        inventario = request.form["inventario"]

        db = get_db()
        db.execute(
            'INSERT INTO product (grupo, serie, codigo, nombre, descripcion,'
            ' marca, imagen, mi_precio, precio_venta, inventario)'
            ' VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', (grupo, serie, codigo, nombre,
            descripcion, marca, imagen, mi_precio, precio_venta, inventario)
        )
        db.commit()
        save_image(current_app, imagen_file)

        return redirect(url_for('inventory.inventory'))

    return render_template('inventory/add_product.html', heads=heads)


def remove_image(current_app, image_name):
    images_path = os.path.join(current_app.root_path, "static/images")
    image_path = os.path.join(images_path, image_name)
    os.remove(image_path)


@bp.route('/<string:codigo>/update_product', methods=('GET', 'POST'))
def update_product(codigo):
    product = get_product(codigo)

    if request.method == 'POST':
        grupo = request.form["grupo"]
        serie = request.form["serie"]
        nombre = request.form["nombre"]
        descripcion = request.form["descripcion"] 
        marca = request.form["marca"]
        imagen_file = request.files["imagen"]
        imagen = imagen_file.filename
        mi_precio = request.form["mi_precio"]
        precio_venta = request.form["precio_venta"]
        inventario = request.form["inventario"]

        error = None

        if not grupo:
            error = 'Grupo es requerido'

        if error is not None:
            flash(error)
        else:
            if not imagen_file:
                imagen = product["imagen"]
            else:
                remove_image(current_app, product["imagen"])
                save_image(current_app, imagen_file)

            db = get_db()
            db.execute(
                'UPDATE product SET grupo = ?, serie = ?, nombre = ?, descripcion = ?,'
                ' marca = ?, imagen = ?, mi_precio = ?, precio_venta = ?,'
                ' inventario = ? WHERE codigo = ?', (grupo, serie, nombre, descripcion,
                marca, imagen, mi_precio, precio_venta, inventario, codigo)
            )
            db.commit()

            return redirect(url_for('inventory.inventory'))

    return render_template('inventory/update_product.html', product=product, heads=heads)


@bp.route('/<string:codigo>/remove_product', methods=('POST',))
def remove_product(codigo):
    db = get_db()
    product = get_product(codigo)
    remove_image(current_app, product["imagen"])
    db.execute('DELETE FROM product WHERE codigo = ?', (codigo,))
    db.commit()

    return redirect(url_for('inventory.inventory'))
