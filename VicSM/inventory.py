from flask import (
    Blueprint, render_template, request, redirect,
    url_for, flash
)
from VicSM.models import save_image, remove_image, Product, add_item
from VicSM import db

bp = Blueprint('inventory', __name__)

heads = {
    "grupo": "Grupo", "serie": "Serie", "codigo": "Código",
    "nombre": "Nombre", "descripcion": "Descripción",
    "marca": "Marca", "imagen": "Imagen", "mi_precio": "Precio Compra",
    "precio_venta": "Precio Venta", "inventario": "Inv."
}
search_heads = {}
for head in heads:
    if head != "descripcion" and head != "imagen":
        search_heads[head] = heads[head]

inv_heads = {}
for head in heads:
    if head != "grupo" and head != "serie" and head != "descripcion":
        inv_heads[head] = heads[head]


@bp.route('/inventory', methods=('POST', 'GET'))
def inventory():
    products = Product.query.all()
    autocomplete_inv = get_autocomplete_data(products)
    if request.method == 'POST':
        search_term = request.form["search_term"]
        products = get_products(search_term)
        if not products:
            products = Product.query.all()

    return render_template(
        'inventory/inventory.html', products=products,
        heads=inv_heads, format_price=format_price,
        autocomplete_inv=autocomplete_inv
    )


@bp.route('/add_product', methods=('GET', 'POST'))
def add_product():
    form_values = {}
    for key in heads:
        if key != "imagen":
            form_values[key] = ""

    if request.method == 'POST':
        imagen_file = request.files["imagen"]
        imagen = imagen_file.filename
        if not imagen:
            imagen = "default.png"
        for key in form_values:
            form_values[key] = request.form[key]
        error = None

        try:
            float(form_values["mi_precio"])
            float(form_values["precio_venta"])
            int(form_values["inventario"])
        except ValueError:
            error = "Introdujo un número invalido"

        if not error:
            product = Product(
                grupo=form_values["grupo"],
                serie=form_values["serie"],
                codigo=form_values["codigo"],
                nombre=form_values["nombre"],
                descripcion=form_values["descripcion"],
                marca=form_values["marca"],
                imagen=imagen,
                mi_precio=form_values["mi_precio"],
                precio_venta=form_values["precio_venta"],
                inventario=form_values["inventario"],
                inv_ref=form_values["inventario"]
            )
            error = add_item(product)
            if not error:
                save_image(imagen_file)
                return redirect(url_for('inventory.inventory'))

        flash(error)

    return render_template(
        'inventory/add_product.html', heads=heads,
        form_values=form_values
    )


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
        error = None

        try:
            float(product.mi_precio)
            float(product.precio_venta)
            int(product.inventario)
        except ValueError:
            error = "Introdujo un número invalido"

        if not error:
            if imagen_file:
                product.imagen = imagen_file.filename
                remove_image(product.imagen)
                save_image(imagen_file)
            db.session.commit()
            return redirect(url_for('inventory.inventory'))

        flash(error)

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


def format_price(num):
    if not num:
        num = 0
    num = round(num, 2)
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


def get_products(search_term=None):
    products = Product.query.filter_by(codigo=search_term).all()
    if not products:
        products = Product.query.filter_by(grupo=search_term).all()
    if not products:
        products = Product.query.filter_by(serie=search_term).all()
    if not products:
        products = Product.query.filter_by(nombre=search_term).all()
    if not products:
        products = Product.query.filter_by(marca=search_term).all()
    if not products:
        products = Product.query.all()

    return products


def get_product(search_term):
    product = Product.query.filter_by(codigo=search_term).first()
    if not product:
        product = Product.query.filter_by(nombre=search_term).first()

    return product


def get_autocomplete_data(products):
    autocomplete_data = []
    for product in products:
        if product.grupo not in autocomplete_data:
            autocomplete_data.append(product.grupo)
        if product.serie not in autocomplete_data:
            autocomplete_data.append(product.serie)
        if product.marca not in autocomplete_data:
            autocomplete_data.append(product.marca)
        autocomplete_data.append(product.nombre)
        autocomplete_data.append(product.codigo)

    autocomplete_data = sorted(autocomplete_data)

    return autocomplete_data
