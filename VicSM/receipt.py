from flask import (
    Blueprint, render_template, request
)
from VicSM.inventory import get_product, format_price, add_iva

bp = Blueprint('receipt', __name__)

heads = {
    "codigo": "Código", "nombre": "Nombre", "descripcion": "Descripción", "marca": "Marca", 
    "imagen": "Imagen", "precio_venta": "Precio Venta", "mas_iva": "Mas Iva", "cantidad": "Cantidad",
    "total": "Total"
}


def get_total(totals):
    total = 0
    for key in totals:
        total += totals[key]

    return round(total, 2)   


products = {}
totals = {}
cantidades = {}


@bp.route('/receipt', methods=('GET', 'POST'))
def receipt():
    empty_product = {}
    global totals
    global cantidades
    global products

    for head in heads:
        empty_product[head] = ""


    if request.method == "POST":
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

        codigo = request.form["codigo"]
        product = get_product(codigo)
        if product is not None:
            products[codigo] = product

        total = get_total(totals)

    elif request.method == "GET":
        total = 0
        products = {}
        cantidades = {}
        totals = {}
            

    return render_template('receipt/receipt.html', heads=heads, 
        products=products, empty_product=empty_product, totals=totals, total=total,
        cantidades= cantidades, format_price=format_price, add_iva=add_iva)


@bp.route('/receipts', methods=('GET', 'POST'))
def receipts():

    return render_template('client/receipts.html')