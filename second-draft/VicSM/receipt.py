from flask import (
    Blueprint, g, render_template, request
)
from VicSM.inventory import get_product

bp = Blueprint('receipt', __name__)

heads = [
    "codigo", "nombre", "descripcion", "marca", 
    "imagen", "precio_venta", "cantidad", "total"
    ]
products = []


@bp.route('/receipt', methods=('GET', 'POST'))
def receipt():
    empty_product = {}

    for head in heads:
        empty_product[head] = ""


    if request.method == "POST":
        codigo = request.form["codigo"]
        try:
            cantidad = request.form["cantidad"]
        except KeyError:
            pass

        product = get_product(codigo)
        products.append(product)

    return render_template('receipt/receipt.html', heads=heads, products=products, empty_product=empty_product)