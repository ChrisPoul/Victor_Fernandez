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
    page = request.args.get('page', 1, type=int)
    products = Product.query.paginate(page=page, per_page=2)
    autocomplete_inv = get_autocomplete_data()
    if request.method == 'POST':
        search_term = request.form["search_term"]
        return redirect(
            url_for('inventory.inventory_search', search_term=search_term)
        )

    return render_template(
        'inventory/inventory.html',
        products=products,
        products_lst=products.items,
        format_price=format_price,
        autocomplete_inv=autocomplete_inv,
        heads=inv_heads
    )


@bp.route('/inventory_search/<string:search_term>')
def inventory_search(search_term):
    products = get_products(search_term)

    if not products:
        return redirect(
            url_for('inventory.inventory')
        )

    return render_template(
        'inventory/inventory_search.html',
        products_lst=products,
        heads=inv_heads, format_price=format_price
    )


@bp.route('/add_product', methods=('GET', 'POST'))
def add_product():
    form = create_new_form()
    for key in heads:
        if key != "imagen":
            form[key] = ""

    if request.method == 'POST':
        imagen_file = request.files["imagen"]
        imagen = imagen_file.filename
        if not imagen:
            imagen = "default.png"
        error = None

        error = validate_form_numbers(request.form)

        if not error:
            product = Product(
                grupo=request.form["grupo"],
                serie=request.form["serie"],
                codigo=request.form["codigo"],
                nombre=request.form["nombre"],
                descripcion=request.form["descripcion"],
                marca=request.form["marca"],
                imagen=imagen,
                mi_precio=request.form["mi_precio"],
                precio_venta=request.form["precio_venta"],
                inventario=request.form["inventario"],
                inv_ref=request.form["inventario"]
            )
            error = add_item(product)
            if not error:
                save_image(imagen_file)
                return redirect(url_for('inventory.inventory'))

        flash(error)

    return render_template(
        'inventory/add_product.html', heads=heads,
        form=request.form
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

        error = validate_form_numbers(request.form)

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

    num_int, num_dec = num.split(".")
    if len(num_dec) == 1:
        num_dec += "0"

    num_int = add_commas_to_num(num_int)
    num = f"${num_int}.{num_dec}"

    return num


def add_commas_to_num(num_str):
    comma_track = 1
    int_with_commas = ""
    for i, num in enumerate(num_str[::-1]):
        int_with_commas += num
        if comma_track == 3 and i != len(num_str)-1:
            int_with_commas += ","
            comma_track = 0
        comma_track += 1

    return int_with_commas[::-1]


def add_iva(num):
    num = round(float(num) * 1.16, 2)

    return format_price(num)


def create_new_form():
    form = {}
    for key in heads:
        if key != "imagen":
            form[key] = ""

    return form


def validate_form_numbers(form):
    error = None
    try:
        float(form["mi_precio"])
        float(form["precio_venta"])
        int(form["inventario"])
    except ValueError:
        error = "Introdujo un número invalido"

    return error


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


def get_product(search_term):
    product = Product.query.filter_by(codigo=search_term).first()
    if not product:
        product = Product.query.filter_by(nombre=search_term).first()

    return product


def get_autocomplete_data():
    products = Product.query.all()
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
