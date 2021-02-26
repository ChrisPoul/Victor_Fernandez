import math
import base64
from io import BytesIO
from flask import (
    Blueprint, render_template
)
from operator import attrgetter
from datetime import datetime
from matplotlib.figure import Figure
from VicSM.models import (
    Product, Client, format_date, days
)
from VicSM.inventory import add_iva


bp = Blueprint('main_page', __name__)


def get_graphs_figure():
    fig = Figure(dpi=220)
    axs = fig.subplots(nrows=2, ncols=2)

    axs[0, 0].plot([2, 3, 3, 2])
    axs[0, 0].set_title('Ganancias del mes')
    axs[0, 1].plot([1, 4])
    axs[0, 1].set_title('Ganancias de la semana')
    axs[1, 0].plot([3, 4, 1])
    axs[1, 0].set_title('Ventas del mes')
    axs[1, 1].plot([3, 1, 1])
    axs[1, 1].set_title('Ventas de la semana')

    # Hide x labels and tick labels for top plots and y ticks for right plots.
    for ax in axs.flat:
        ax.label_outer()

    # Save figuro to a temporary buffer.
    buf = BytesIO()
    fig.savefig(buf, format="png")
    # Embed the result in the html output.
    data = base64.b64encode(buf.getbuffer()).decode("ascii")

    return data


@bp.route('/')
def main_page():
    clients = get_recent_clients()
    recent_receipts = get_recent_receipts(clients)
    products = Product.query.all()
    columns = range(math.ceil(len(clients)/2))
    rows = range(2)
    data = get_graphs_figure()

    return render_template(
        'main_page/main_page.html', len=len,
        products=products, columns=columns,
        format_date=format_date, rows=rows,
        receipts=recent_receipts,
        clients=clients, add_iva=add_iva,
        format_time=format_time, data=data
    )


def format_time(time):
    hour = str(time.hour)
    minute = str(time.minute)
    if len(hour) == 1:
        hour = "0" + hour
    if len(minute) == 1:
        minute = "0" + minute

    day = time.weekday()
    today = datetime.now().weekday()
    if day == today:
        day = "Hoy"
    elif day == today-1:
        day = "Ayer"
    else:
        day = days[str(day)]

    if hour == "01":
        formated_time = f"{day} a la {hour}:{minute}"
    else:
        formated_time = f"{day} a las {hour}:{minute}"

    return formated_time


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
    receipts_sorted = sorted(
        recent_receipts, key=attrgetter('fecha'), reverse=True)
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
