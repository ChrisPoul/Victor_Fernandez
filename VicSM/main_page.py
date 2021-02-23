from flask import (
    Blueprint, render_template
)
from VicSM.inventory import get_product

bp = Blueprint('main_page', __name__)


@bp.route('/')
def main_page():
    recent_receipts = {}
    clients = []

    codigos_frecuentes = []
    products = {}
    for codigo in codigos_frecuentes:
        product = get_product(codigo)
        products[codigo] = product

    return render_template(
        'main_page/main_page.html', receipts=recent_receipts, clients=clients,
        products=products
    )
