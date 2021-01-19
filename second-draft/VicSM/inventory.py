from flask import (
    Blueprint, g, render_template, request, flash, redirect, url_for
)
from VicSM.db import get_db

bp = Blueprint('inventory', __name__, url_prefix='/inventory')
heads = [
    "codigo", "nombre", "descripcion", "marca", 
    "imagen", "mi_precio", "precio_venta", "inventario"
    ]


@bp.route('/')
def inventory():
    db = get_db()
    products = db.execute(
        'SELECT p.codigo, grupo, serie, nombre, descripcion,'
        ' marca, imagen, mi_precio, precio_venta, inventario'
        ' FROM product p'
    ).fetchall()

    return render_template('inventory/inventory.html', products=products, heads=heads)


@bp.route('/add_product', methods=('GET', 'POST'))
def add_product():
    if request.method == 'POST':
        grupo = request.form["grupo"]
        serie = request.form["serie"]
        codigo = request.form["codigo"]
        nombre = request.form["nombre"]
        descripcion = request.form["descripcion"] 
        marca = request.form["marca"]
        imagen = request.form["imagen"]
        mi_precio = request.form["mi_precio"]
        precio_venta = request.form["precio_venta"]
        inventario = request.form["inventario"]

        error = None

        if not codigo or not nombre:
            error = "Falta llenar cosas"

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO product (grupo, serie, codigo, nombre, descripcion,'
                ' marca, imagen, mi_precio, precio_venta, inventario)'
                ' VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', (grupo, serie, codigo, nombre,
                descripcion, marca, imagen, mi_precio, precio_venta, inventario)
            )
            db.commit()

            return redirect(url_for('inventory.inventory'))

    return render_template('inventory/add_product.html')


def get_product(codigo):
    db = get_db()
    product = db.execute(
        'SELECT * FROM product WHERE codigo = ?', (codigo,)
    ).fetchone()

    return product


@bp.route('/<string:codigo>/update_product', methods=('GET', 'POST'))
def update_product(codigo):
    product = get_product(codigo)

    if request.method == 'POST':
        grupo = request.form["grupo"]
        serie = request.form["serie"]
        descripcion = request.form["descripcion"] 
        marca = request.form["marca"]
        imagen = request.form["imagen"]
        mi_precio = request.form["mi_precio"]
        precio_venta = request.form["precio_venta"]
        inventario = request.form["inventario"]

        error = None

        if not grupo:
            error = 'Grupo es requerido'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE product SET grupo = ?, serie = ?, descripcion = ?,'
                ' marca = ?, imagen = ?, mi_precio = ?, precio_venta = ?,'
                ' inventario = ? WHERE codigo = ?', (grupo, serie, descripcion,
                marca, imagen, mi_precio, precio_venta, inventario, codigo)
            )
            db.commit()

            return redirect(url_for('inventory.inventory'))

    return render_template('inventory/update_product.html', product=product)


@bp.route('/<string:codigo>/remove_product', methods=('POST',))
def remove_product(codigo):
    db = get_db()
    db.execute('DELETE FROM product WHERE codigo = ?', (codigo))
    db.commit()

    return redirect(url_for('inventory.inventory'))
