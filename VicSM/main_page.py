from flask import (
    Blueprint, request, render_template
)
from VicSM.db import get_receipts
from VicSM.client import get_client
from VicSM.inventory import get_product

bp = Blueprint('main_page', __name__)


@bp.route('/')
def main_page():
    receipts = get_receipts()
    recent_receipts = {}
    clients = []
    for client_id in receipts:
        client_receipts = receipts[client_id]
        recent_receipt_id = client_receipts["numero_de_recibos"]
        recent_receipt = client_receipts[str(recent_receipt_id)]
        client = get_client(client_id)
        clients.append(client)
        client_name = client["nombre"]
        recent_receipts[client_name] = recent_receipt

    codigos_frecuentes = []
    products = {}
    for codigo in codigos_frecuentes:
        product = get_product(codigo)
        products[codigo] = product


    return render_template(
        'main_page/main_page.html', receipts=recent_receipts, clients=clients,
        products=products
        )
