from flask import (
    Blueprint, g, render_template, request
)
from VicSM.inventory import get_product

bp = Blueprint('receipt', __name__)

heads = [
    "codigo", "nombre", "descripcion", "marca", 
    "imagen", "precio_venta", "cantidad", "total"
    ]


def get_total(totals):
    total = 0
    for key in totals:
        total += totals[key]

    return round(total, 2)


products = {}
totals = {}


@bp.route('/receipt', methods=('GET', 'POST'))
def receipt():
    empty_product = {}
    global totals
    global products

    for head in heads:
        empty_product[head] = ""


    if request.method == "POST":
        codigo = request.form["codigo"]
        try:
            for code in products:
                cantidad = request.form[code]
                try:
                    cantidad = int(cantidad)
                except ValueError:
                    cantidad = 0

                product = products[code]
                totals[code] = round(cantidad * product["precio_venta"], 2)
                    
        except KeyError:
            pass

        product = get_product(codigo)
        if product is not None:
            products[codigo] = product

        total = get_total(totals)

    elif request.method == "GET":
        total = 0
        products = {}
        totals = {}
            

    return render_template('receipt/receipt.html', heads=heads, products=products, empty_product=empty_product, totals=totals, total=total)