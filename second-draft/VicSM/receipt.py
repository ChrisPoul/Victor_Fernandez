from flask import (
    Blueprint, g, render_template
)

bp = Blueprint('receipt', __name__)

heads = [
    "codigo", "nombre", "descripcion", "marca", 
    "imagen", "mi_precio", "precio_venta", "inventario"
    ]


@bp.route('/receipt', methods=('GET', 'POST'))
def receipt():

    return render_template('receipt/receipt.html', heads=heads)