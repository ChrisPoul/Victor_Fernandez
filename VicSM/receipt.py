import os
import datetime
import glob
import json
from flask import (
    Blueprint, render_template, request, redirect, url_for,
    current_app
)
from VicSM.inventory import get_product, format_price, add_iva
from VicSM.client import get_client, client_heads
from VicSM.db import (
    get_db, get_receipts, save_receipts, format_date, get_receipt,
    save_receipt, get_client_receipts
)

bp = Blueprint('receipt', __name__)

product_heads = {
    "codigo": "Código", "nombre": "Nombre", "descripcion": "Descripción", "marca": "Marca", 
    "imagen": "Imagen", "precio_venta": "Precio Venta", "mas_iva": "Mas Iva", "cantidad": "Cnt.",
    "total": "Total"
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
        cantidades = receipt["cantidades"]
        for code in cantidades: products[code] = get_product(code)

        return products


@bp.route('/<int:client_id>/new_receipt', methods=('GET', 'POST'))
def new_receipt(client_id):
    client = get_client(client_id)

    if request.method == "POST":
        try:
            search_term = request.form['search_term']
            client = get_client(search_term)
        except KeyError:
            pass

    if client:
        client_id = client["id"]
        receipt = get_receipt(client_id, 0)
        save_receipt(client_id, 0, receipt)
        client_receipts = get_client_receipts(client_id)
        receipt_id = client_receipts["numero_de_recibos"]

        return redirect(
            url_for(
                'receipt.edit_receipt', client_id=client["id"], 
                receipt_id=receipt_id
            )
        )
    
    return render_template('receipt/receipt_search.html')


@bp.route('/<int:receipt_id>/<int:client_id>/edit_receipt', methods=('GET', 'POST'))
def edit_receipt(client_id, receipt_id):
    aasm_image = get_aasm_image()
    client = get_client(client_id)
    receipt = get_receipt(client_id, receipt_id)
    products = get_receipt_products(receipt)

    cantidades = receipt["cantidades"]
    grupo = receipt["grupo"]
    cambio= receipt["cambio"]
    if not cambio: cambio = client["cambio"]
    totals = receipt["totals"]
    total = receipt["total"]
    fecha = format_date(datetime.date.today())

    if request.method == "POST":
        try:
            grupo = request.form['grupo']
        except KeyError:
            pass

        try:
            cambio = request.form['cambio']
            try:
                cambio = float(cambio)
            except ValueError:
                cambio = client['cambio']
        except KeyError:
            pass

        for code in products:
            try:
                cantidades[code] = request.form[code]
                try:
                    cantidades[code] = int(cantidades[code])
                except ValueError:
                    cantidades[code] = 0
                product = products[code]
                totals[code] = round(cantidades[code] * float(product["precio_venta"]), 2)
            except KeyError:
                pass

        try:
            codigo = request.form["codigo"]
        except KeyError:
            codigo = ""

        total = get_total(totals)
        product = get_product(codigo)
        if product is not None:
            products[codigo] = product
            cantidades[codigo] = 0

        for code in products:
            try:
                dummy_var = cantidades[code]
            except KeyError:
                cantidades[code] = 0

        receipt["cantidades"] = cantidades
        receipt["grupo"] = grupo
        receipt["cambio"] = cambio
        receipt["totals"] = totals
        receipt["total"] = total
        receipt["fecha"] = fecha
        save_receipt(client_id, receipt_id, receipt)
            
    return render_template(
        'receipt/receipt.html', product_heads=product_heads, client_heads=client_heads,
        products=products, totals=totals, total=total, cantidades=cantidades, grupo=grupo,
        format_price=format_price, add_iva=add_iva, client=client, middle_heads=middle_heads,
        last_heads=last_heads, cambio=cambio, receipt_id=receipt_id, aasm_image=aasm_image,
        fecha=fecha, receipt=receipt
    )


@bp.route('/<int:client_id>/<int:receipt_id>/receipt_done')
def receipt_done(client_id, receipt_id):
    aasm_image = get_aasm_image()
    client = get_client(client_id)
    receipt = get_receipt(client_id, receipt_id)
    products = get_receipt_products(receipt)

    totals = receipt["totals"]
    total = receipt["total"]
    cantidades = receipt["cantidades"]
    grupo = receipt["grupo"]
    cambio = receipt["cambio"]
    fecha = receipt["fecha"]

    return render_template(
        'receipt/receipt_done.html', product_heads=product_heads, client_heads=client_heads,
        products=products, totals=totals, total=total, cantidades=cantidades, grupo=grupo,
        format_price=format_price, add_iva=add_iva, client=client, middle_heads=middle_heads,
        last_heads=last_heads, cambio=cambio, aasm_image=aasm_image, fecha=fecha
    )


@bp.route('/<int:client_id>/<int:receipt_id>/reset_receipt')
def reset_receipt(client_id, receipt_id):
    receipt = get_receipt(client_id, 0)
    save_receipt(client_id, receipt_id, receipt)

    return redirect(
        url_for('receipt.edit_receipt', client_id=client_id, receipt_id= receipt_id)
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
    