import os
from datetime import datetime
import glob
import json
from flask import (
    Blueprint, render_template, request, redirect, url_for,
    current_app
)
from VicSM.inventory import get_product, format_price, add_iva
from VicSM.client import get_client, client_heads
from VicSM.models import (
    format_date, add_item, Client, Receipt
)
from VicSM import db

bp = Blueprint('receipt', __name__)

product_heads = {
    "codigo": "Código", "nombre": "Nombre", "descripcion": "Descripción",
    "marca": "Marca", "imagen": "Imagen", "precio_venta": "Precio Venta",
    "mas_iva": "Mas Iva", "cantidad": "Cnt.", "total": "Total"
}
middle_heads = {
    "nombre": "Nombre del Cliente ó Razón Social", "tel": "Tel/Fax",
    "cambio": "Tipo de Cambio"
}
last_heads = ["direccion", "nombre", "descripcion"]


def get_total(totals):
    total = 0
    for key in totals:
        total += totals[key]

    return round(total, 2)


def get_aasm_image():
    my_images_path = os.path.join(current_app.root_path, "static/my_images")
    references_path = os.path.join(my_images_path, 'references.json')
    with open(references_path) as aasm_reference_file:
        aasm_reference = json.load(aasm_reference_file)
    aasm_image = aasm_reference["aasm"]

    return aasm_image


def get_receipt_products(receipt):
    products = {}
    cantidades = receipt.cantidades
    for code in cantidades:
        products[code] = get_product(code)

    return products


def get_receipt(receipt_id):
    receipt = Receipt.query.get(receipt_id)

    return receipt


@bp.route('/<int:client_id>/new_receipt', methods=('GET', 'POST'))
def new_receipt(client_id):
    client = Client.query.get(client_id)

    if request.method == "POST":
        try:
            search_term = request.form['search_term']
            client = get_client(search_term)
        except KeyError:
            pass

    if client:
        receipt = Receipt(client_id=client_id, cantidades={'SHELLY_1': 0})
        add_item(receipt)

        return redirect(
            url_for(
                'receipt.edit_receipt', client_id=client.id,
                receipt_id=receipt.id
            )
        )

    return render_template('receipt/receipt_search.html')


def obj_as_dict(obj_tuple):
    obj_dict = {}
    for key in obj_tuple:
        obj_dict[key] = obj_tuple[key]

    return obj_dict


@bp.route('/<int:receipt_id>/<int:client_id>/edit_receipt', methods=('GET', 'POST'))
def edit_receipt(client_id, receipt_id):
    aasm_image = get_aasm_image()
    client = get_client(client_id)
    receipt = get_receipt(receipt_id)
    products = get_receipt_products(receipt)

    if not receipt.cambio:
        receipt.cambio = client.cambio
    receipt.fecha = datetime.utcnow()
    cantidades = obj_as_dict(receipt.cantidades)
    totales = obj_as_dict(receipt.totales)

    if request.method == "POST":
        try:
            receipt.grupo = request.form['grupo']
        except KeyError:
            pass

        try:
            cambio = request.form['cambio']
            try:
                receipt.cambio = float(cambio)
            except ValueError:
                receipt.cambio = client.cambio
        except KeyError:
            pass

        try:
            codigo = request.form["codigo"]
        except KeyError:
            codigo = ""

        for code in products:
            try:
                cantidades[code] = request.form[code]
                try:
                    cantidades[code] = int(cantidades[code])
                except ValueError:
                    cantidades[code] = 0
                precio_venta = products[code].precio_venta
                totales[code] = cantidades[code] * precio_venta
            except KeyError:
                pass

        receipt.total = get_total(totales)
        product = get_product(codigo)
        if product is not None:
            products[codigo] = product
            cantidades[codigo] = 0

        receipt.cantidades = cantidades
        receipt.totales = totales
        db.session.commit()

    grupo = receipt.grupo
    cambio = receipt.cambio
    total = receipt.total
    fecha = receipt.fecha

    return render_template(
        'receipt/receipt.html', product_heads=product_heads,
        client_heads=client_heads, products=products, totals=totales,
        total=total, cantidades=cantidades, grupo=grupo,
        format_price=format_price, add_iva=add_iva, client=client,
        middle_heads=middle_heads, last_heads=last_heads, cambio=cambio,
        receipt_id=receipt_id, aasm_image=aasm_image, fecha=format_date(fecha),
        receipt=receipt
    )


@bp.route('/<int:client_id>/<int:receipt_id>/receipt_done')
def receipt_done(client_id, receipt_id):
    aasm_image = get_aasm_image()
    client = get_client(client_id)
    receipt = get_receipt(receipt_id)
    products = get_receipt_products(receipt)

    totales = receipt.totales
    total = receipt.total
    cantidades = receipt.cantidades
    grupo = receipt.grupo
    cambio = receipt.cambio
    fecha = receipt.fecha

    return render_template(
        'receipt/receipt_done.html', product_heads=product_heads,
        client_heads=client_heads, products=products, totals=totales,
        total=total, cantidades=cantidades, grupo=grupo,
        format_price=format_price, add_iva=add_iva, client=client,
        middle_heads=middle_heads, last_heads=last_heads, cambio=cambio,
        aasm_image=aasm_image, fecha=format_date(fecha)
    )


@bp.route('/<int:client_id>/<int:receipt_id>/reset_receipt')
def reset_receipt(client_id, receipt_id):
    receipt = get_receipt(receipt_id)
    receipt.grupo = None
    receipt.cambio = None
    receipt.totales = {}
    receipt.total = 0
    receipt.cantidades = {}
    db.session.commit()

    return redirect(
        url_for('receipt.edit_receipt',
                client_id=client_id, receipt_id=receipt_id)
    )


def save_my_image(image_file):
    images_path = os.path.join(current_app.root_path, "static/my_images")
    all_images_path = os.path.join(images_path, "*")
    all_images = glob.glob(all_images_path)
    for image in all_images:
        os.remove(image)

    image_name = image_file.filename
    image_path = os.path.join(images_path, image_name)
    image_file.save(image_path)

    references_path = os.path.join(images_path, 'references.json')
    json_references = json.dumps({"aasm": image_name})
    with open(references_path, "w") as references_file:
        references_file.write(json_references)


@bp.route('/receipt_config', methods=('GET', 'POST'))
def receipt_config():
    if request.method == 'POST':
        my_image_file = request.files["imagen"]
        save_my_image(my_image_file)

        return redirect(url_for('receipt.receipt'))

    return render_template('receipt/receipt_config.html')
