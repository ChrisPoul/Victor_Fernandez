from flask import (
    Blueprint, render_template, request, redirect, url_for
)
from VicSM.models import save_image, remove_image, Product, add_item
from VicSM import db

bp = Blueprint('inventory', __name__)

heads = {
    "grupo": "Grupo", "serie": "Serie", "codigo": "Código",
    "nombre": "Nombre", "descripcion": "Descripción",
    "marca": "Marca", "imagen": "Imagen", "mi_precio": "Mi Precio",
    "precio_venta": "Precio Venta", "inventario": "Inventario"
}
search_heads = {}
for head in heads:
    if head != "descripcion" and head != "imagen":
        search_heads[head] = heads[head]


def format_price(num):
    if not num:
        num = 0

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
    products = Product.query.filter_by(codigo=search_term).all()
    if not products:
        products = Product.query.filter_by(grupo=search_term).all()
    if not products:
        products = Product.query.filter_by(serie=search_term).all()
    if not products:
        products = Product.query.filter_by(nombre=search_term).all()
    if not products:
        products = Product.query.filter_by(marca=search_term).all()

    return products


def get_product(codigo):
    product = Product.query.filter_by(codigo=codigo).first()

    return product


@bp.route('/inventory', methods=('POST', 'GET'))
def inventory():
    products = Product.query.all()
    if request.method == 'POST':
        search_term = request.form["search_term"]
        products = get_products(search_term)
        if not products:
            products = Product.query.all()

    return render_template(
        'inventory/inventory.html', products=products, heads=heads,
        format_price=format_price
    )


@bp.route('/add_product', methods=('GET', 'POST'))
def add_product():
    if request.method == 'POST':
        imagen_file = request.files["imagen"]
        product = Product(
            grupo=request.form["grupo"],
            serie=request.form["serie"],
            codigo=request.form["codigo"],
            nombre=request.form["nombre"],
            descripcion=request.form["descripcion"],
            marca=request.form["marca"],
            imagen=imagen_file.filename,
            mi_precio=request.form["mi_precio"],
            precio_venta=request.form["precio_venta"],
            inventario=request.form["inventario"]
        )
        add_item(product)
        save_image(imagen_file)

        return redirect(url_for('inventory.inventory'))

    return render_template('inventory/add_product.html', heads=heads)


@bp.route('/<string:codigo>/update_product', methods=('GET', 'POST'))
def update_product(codigo):
    product = get_product(codigo)

    if request.method == 'POST':
        imagen_file = request.files["imagen"]
        product.grupo = request.form["grupo"]
        product.serie = request.form["serie"]
        product.nombre = request.form["nombre"]
        product.descripcion = request.form["descripcion"]
        product.marca = request.form["marca"]
        product.mi_precio = request.form["mi_precio"]
        product.precio_venta = request.form["precio_venta"]
        product.inventario = request.form["inventario"]
        if not imagen_file:
            product.imagen = product.imagen
        else:
            product.imagen = imagen_file.filename
            remove_image(product.imagen)
            save_image(imagen_file)

        db.session.commit()

        return redirect(url_for('inventory.inventory'))

    return render_template(
        'inventory/update_product.html', product=product, heads=heads
    )


@bp.route('/<string:codigo>/remove_product', methods=('POST',))
def remove_product(codigo):
    product = get_product(codigo)
    db.session.delete(product)
    db.session.commit()
    remove_image(product.imagen)

    return redirect(url_for('inventory.inventory'))
