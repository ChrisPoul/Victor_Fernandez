from flask import (
    Blueprint, render_template, request
)
from VicSM.inventory import get_product, format_price, add_iva
from VicSM.client import get_client, client_heads

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


client = None
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

    if request.method == "POST":
        if not client or not grupo or not cambio:
            try:
                search_term = request.form['search_term']
                client = get_client(search_term)
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

    elif request.method == "GET":
        client = None
        grupo = None
        cambio = None
        products = {}
        cantidades = {}
        totals = {}
        total = 0
            
    return render_template(
        'receipt/receipt.html', product_heads=product_heads, client_heads=client_heads,
        products=products, totals=totals, total=total, cantidades=cantidades, grupo=grupo,
        format_price=format_price, add_iva=add_iva, client=client, middle_heads=middle_heads,
        last_heads=last_heads, cambio=cambio
    )


@bp.route('/receipt_done')
def receipt_done():

    return render_template(
        'receipt/receipt_done.html', product_heads=product_heads, client_heads=client_heads,
        products=products, totals=totals, total=total, cantidades=cantidades, grupo=grupo,
        format_price=format_price, add_iva=add_iva, client=client, middle_heads=middle_heads,
        last_heads=last_heads
        )
