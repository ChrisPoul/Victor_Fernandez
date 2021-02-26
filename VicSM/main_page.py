import math
from flask import (
    Blueprint, render_template
)
from operator import attrgetter
from VicSM.models import (
    Product, Client, format_date
)

bp = Blueprint('main_page', __name__)


def get_recent_receipts(clients):
    recent_receipts = []
    for client in clients:
        client_receipts = client.recibos
        if client_receipts:
            receipts_sorted = sorted(client_receipts, key=attrgetter('fecha'))
            receipt = receipts_sorted[-1]
            recent_receipts.append(receipt)

    return recent_receipts


def get_recent_clients():
    clients = Client.query.all()
    recent_receipts = get_recent_receipts(clients)
    receipts_sorted = sorted(recent_receipts, key=attrgetter('fecha'), reverse=True)
    if len(receipts_sorted) <= 6:
        index = len(receipts_sorted)
    else:
        index = 6

    recent_clients = []
    for receipt in receipts_sorted[:index]:
        client = receipt.author
        if client not in recent_clients:
            recent_clients.append(client)

    return recent_clients


@bp.route('/')
def main_page():
    clients = get_recent_clients()
    recent_receipts = get_recent_receipts(clients)
    products = Product.query.all()
    columns = range(math.ceil(len(clients)/2))
    rows = range(2)

    return render_template(
        'main_page/main_page.html', len=len,
        products=products, columns=columns,
        format_date=format_date, rows=rows,
        receipts=recent_receipts,
        clients=clients
    )
