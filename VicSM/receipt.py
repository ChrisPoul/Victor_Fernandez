from flask import (
    Blueprint, render_template, request
)
from VicSM.inventory import get_product, format_price, add_iva
from VicSM.client import get_client, client_heads

bp = Blueprint('receipt', __name__)

product_heads = {
    "codigo": "Código", "nombre": "Nombre", "descripcion": "Descripción", "marca": "Marca", 
    "imagen": "Imagen", "precio_venta": "Precio Venta", "mas_iva": "Mas Iva", "cantidad": "Cantidad",
    "total": "Total"
    }


def get_total(totals):
    total = 0
    for key in totals:
        total += totals[key]

    return round(total, 2)   


client = None
products = {}
totals = {}
cantidades = {}


@bp.route('/receipt', methods=('GET', 'POST'))
def receipt():
    empty_product = {}
    global client
    global totals
    global cantidades
    global products

    for head in product_heads:
        empty_product[head] = ""


    if request.method == "POST":
        try:
            client_id = request.form['client_id']
            try:
                client_id = int(client_id)
            except ValueError:
                client_id = 0

            client = get_client(client_id)

        except KeyError:
            pass

        try:
            for code in products:
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

        product = get_product(codigo)
        if product is not None:
            products[codigo] = product

        total = get_total(totals)

    elif request.method == "GET":
        total = 0
        client = None
        products = {}
        cantidades = {}
        totals = {}
            

    return render_template(
        'receipt/receipt.html', product_heads=product_heads, client_heads=client_heads,
        products=products, empty_product=empty_product, totals=totals, total=total,
        cantidades=cantidades, format_price=format_price, add_iva=add_iva, client=client
        )


@bp.route('/receipts', methods=('GET', 'POST'))
def receipts():

    return render_template('client/receipts.html')