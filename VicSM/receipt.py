from flask import (
    Blueprint, render_template, request, redirect, url_for
)
from VicSM.inventory import get_product, format_price, add_iva
from VicSM.client import get_client, client_heads
from VicSM.db import get_db, get_receipts, save_receipts

bp = Blueprint('receipt', __name__)

product_heads = {
    "codigo": "Código", "nombre": "Nombre", "descripcion": "Descripción", "marca": "Marca", 
    "imagen": "Imagen", "precio_venta": "Precio Venta", "mas_iva": "Mas Iva", "cantidad": "Cnt.",
    "total": "Total"
    }
middle_heads = {
    "nombre": "Nombre del Cliente ó Razón Social", "tel": "Tel/Fax", 
    "hoja": "Hoja", "cambio": "Tipo de Cambio"
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


client = {"id": 0}
grupo = None
cambio = None
products = {}
totals = {}
total = 0
cantidades = {}


@bp.route('/receipt', methods=('GET', 'POST'))
def receipt():
    global client
    global grupo
    global cambio
    global totals
    global total
    global cantidades
    global products
    receipt_id = 0

    if request.method == "GET":
        client = {"id": 0}
        products = {}

    elif request.method == "POST":
        try:
            search_term = request.form['search_term']
            client = get_client(search_term)
            if not client:
                client = {"id": 0}
            else:
                cambio = client["cambio"]
        except KeyError:
            client = client

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
        last_heads=last_heads, cambio=cambio, receipt_id=receipt_id
    )


@bp.route('/<int:client_id>/<int:receipt_id>/receipt_done')
def receipt_done(client_id, receipt_id):
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
            "grupo": grupo, "cambio": cambio
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
        last_heads=last_heads, cambio=cambio
        )


@bp.route('/reset_receipt')
def reset_receipt():
    global grupo
    global cambio
    global totals
    global total
    global cantidades

    grupo = None
    cambio = None
    cantidades = {}
    totals = {}
    total = 0

    return redirect(url_for('receipt.receipt'))


@bp.route('/<int:receipt_id>/<int:client_id>/receipt', methods=('GET', 'POST'))
def edit_receipt(client_id, receipt_id):
    global client
    global grupo
    global cambio
    global totals
    global total
    global cantidades
    global products

    receipt = get_receipt(client_id, receipt_id)
    client = get_client(client_id)
    grupo = receipt["grupo"]
    cambio= receipt["cambio"]
    totals = receipt["totals"]
    total = receipt["total"]
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
        last_heads=last_heads, cambio=cambio, receipt_id=receipt_id
    )