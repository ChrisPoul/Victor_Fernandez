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
from VicSM.db import get_db, get_receipts, save_receipts, format_date

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


def get_receipt(client_id, receipt_id):
    receipts = get_receipts()
    client_receipts = receipts[str(client_id)]

    return client_receipts[str(receipt_id)]


def get_aasm_image():
    my_images_path = os.path.join(current_app.root_path, "static/my_images")
    references_path = os.path.join(my_images_path, 'references.json')
    with open(references_path) as aasm_reference_file:
        aasm_reference = json.load(aasm_reference_file)
    aasm_image = aasm_reference["aasm"]

    return aasm_image

client = None
grupo = None
cambio = None
products = {}
totals = {}
total = 0
cantidades = {}
fecha = format_date(datetime.date.today())


@bp.route('/<int:client_id>/receipt', methods=('GET', 'POST'))
def receipt(client_id):
    global client
    global grupo
    global cambio
    global totals
    global total
    global cantidades
    global products
    global fecha
    receipt_id = 0
    aasm_image = get_aasm_image()
    if not client:
        client = get_client(client_id)
    
    if client:
        cambio = client["cambio"]

    if request.method == "GET":
        products = {}
        grupo = None
        client = None
        cantidades = {}
        totals = {}
        total = 0
        fecha = format_date(datetime.date.today())

    elif request.method == "POST":
        try:
            search_term = request.form['search_term']
            client = get_client(search_term)
            if client:
                cambio = client["cambio"]
        except KeyError:
            pass

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

        for code in products:
            try:
                dummy_var = cantidades[code]
            except KeyError:
                cantidades[code] = 0
            
    return render_template(
        'receipt/receipt.html', product_heads=product_heads, client_heads=client_heads,
        products=products, totals=totals, total=total, cantidades=cantidades, grupo=grupo,
        format_price=format_price, add_iva=add_iva, client=client, middle_heads=middle_heads,
        last_heads=last_heads, cambio=cambio, receipt_id=receipt_id, aasm_image=aasm_image,
        fecha=fecha
    )


@bp.route('/<int:client_id>/<int:receipt_id>/receipt_done')
def receipt_done(client_id, receipt_id):
    aasm_image = get_aasm_image()
    client = get_client(client_id)
    
    if request.method == "GET":
        receipts = get_receipts()
        client_id = str(client_id)
        try:
            client_receipts = receipts[client_id]
        except KeyError:
            client_receipts = {"numero_de_recibos": 0}

        receipt = {
            "totals": totals, "total": total,
            "cantidades": cantidades, 
            "grupo": grupo, "cambio": cambio,
            "fecha": fecha
            }
        if receipt_id == 0:
            receipt_id = client_receipts["numero_de_recibos"] + 1
            client_receipts["numero_de_recibos"] += 1
            
        client_receipts[str(receipt_id)] = receipt
        receipts[client_id] = client_receipts
        save_receipts(receipts)

    return render_template(
        'receipt/receipt_done.html', product_heads=product_heads, client_heads=client_heads,
        products=products, totals=totals, total=total, cantidades=cantidades, grupo=grupo,
        format_price=format_price, add_iva=add_iva, client=client, middle_heads=middle_heads,
        last_heads=last_heads, cambio=cambio, aasm_image=aasm_image, fecha=fecha
        )


@bp.route('/reset_receipt')
def reset_receipt():
    global client
    global grupo
    global cambio
    global totals
    global total
    global cantidades
    global fecha

    client = None
    grupo = None
    cambio = None
    cantidades = {}
    totals = {}
    total = 0
    fecha = format_date(datetime.date.today())

    return redirect(url_for('receipt.receipt'))


@bp.route('/<int:receipt_id>/<int:client_id>/receipt', methods=('GET', 'POST'))
def edit_receipt(client_id, receipt_id):
    global grupo
    global cambio
    global totals
    global total
    global cantidades
    global products

    aasm_image = get_aasm_image()
    receipt = get_receipt(client_id, receipt_id)
    client = get_client(client_id)
    grupo = receipt["grupo"]
    cambio= receipt["cambio"]
    totals = receipt["totals"]
    total = receipt["total"]
    fecha = format_date(datetime.date.today())
    cantidades = receipt["cantidades"]
    for code in cantidades:
        products[code] = get_product(code)

    if request.method == "POST":
        try:
            grupo = request.form['grupo']
        except KeyError:
            grupo = grupo

        try:
            cambio = request.form['cambio']
            try:
                cambio = float(cambio)
            except ValueError:
                cambio = client['cambio']
        except KeyError:
            cambio = cambio

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

        for code in products:
            try:
                dummy_var = cantidades[code]
            except KeyError:
                cantidades[code] = 0
            
    return render_template(
        'receipt/receipt.html', product_heads=product_heads, client_heads=client_heads,
        products=products, totals=totals, total=total, cantidades=cantidades, grupo=grupo,
        format_price=format_price, add_iva=add_iva, client=client, middle_heads=middle_heads,
        last_heads=last_heads, cambio=cambio, receipt_id=receipt_id, aasm_image=aasm_image,
        fecha=fecha
    )


def save_my_image(image_file):
    images_path = os.path.join(current_app.root_path, "static/my_images")
    image_name = image_file.filename
    image_path = os.path.join(images_path, image_name)
    all_images_path = os.path.join(images_path, "*")
    all_images = glob.glob(all_images_path)
    for image in all_images:
        os.remove(image)
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
    