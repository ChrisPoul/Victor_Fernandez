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

product_heads = {
    "imagen": "Imagen",
    "codigo": "Codigo", "nombre": "Nombre",
    "unidades_vendidas": "Ventas"
}


@bp.route('/')
def main_page():
    clients = get_recent_clients()
    recent_receipts = get_recent_receipts(clients)
    products = get_most_sold_products()[:-1]
    columns = range(math.ceil(len(clients)/2))
    rows = range(2)
    clients_data = get_clients_figure()
    products_data = get_products_figure()
    summary_data = get_summary_figure()

    return render_template(
        'main_page/main_page.html', len=len,
        products=products, columns=columns,
        format_date=format_date, rows=rows,
        receipts=recent_receipts,
        clients_data=clients_data,
        products_data=products_data,
        summary_data=summary_data,
        clients=clients, add_iva=add_iva,
        format_time=format_time,
        product_heads=product_heads
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

    recent_clients = []
    for receipt in receipts_sorted[:6]:
        client = receipt.author
        recent_clients.append(client)

    return recent_clients


def get_most_spending_clients():
    clients = Client.query.all()
    clients = sorted(clients, key=attrgetter('total'), reverse=True)

    clients_names = []
    clients_totals = []
    for client in clients[:6]:
        clients_names.append(client.nombre)
        clients_totals.append(client.total * 1.16)

    return clients_names, clients_totals


def get_clients_figure():
    fig = Figure(dpi=200)
    ax = fig.subplots()
    clients_names, clients_totals = get_most_spending_clients()
    ax.bar(clients_names, clients_totals)
    ax.set_title('Cleintes Más Importantes')
    ax.set_ylabel("Dolares")

    # Save figure to a temporary buffer.
    buf = BytesIO()
    fig.savefig(buf, format="png")
    # Embed the result in the html output.
    data = base64.b64encode(buf.getbuffer()).decode("ascii")

    return data


class Other:

    def __init__(self, unidades_vendidas):
        self.codigo = "Otros"
        self.nombre = "Otros"
        self.imagen = "default.png"
        self.unidades_vendidas = unidades_vendidas


def get_most_sold_products():
    products = Product.query.all()
    products = sorted(products, key=attrgetter(
        "unidades_vendidas"), reverse=True)
    ms_products = []
    others_unidades_vendidas = 0
    for i, product in enumerate(products):
        if product.unidades_vendidas > 0 and i < 8:
            ms_products.append(product)
        else:
            others_unidades_vendidas += product.unidades_vendidas
    ms_products.append(Other(others_unidades_vendidas))

    return ms_products


def get_sold_products():
    products = get_most_sold_products()
    sold_products = []
    sold_units = []
    for product in products:
        sold_products.append(product.nombre)
        sold_units.append(product.unidades_vendidas)

    return sold_products, sold_units


def get_products_figure():
    fig = Figure(dpi=200)
    ax = fig.subplots()
    products_sold, units_sold = get_sold_products()
    ax.pie(units_sold, labels=products_sold)
    ax.set_title('Productos Vendidos')

    buf = BytesIO()
    fig.savefig(buf, format="png")
    data = base64.b64encode(buf.getbuffer()).decode("ascii")

    return data


def get_summary_figure():
    fig = Figure(dpi=220)
    axs = fig.subplots(ncols=2)

    axs[0].plot([1, 2])
    axs[0].set_title("Producción de la Semana")

    axs[1].plot([2, 1])
    axs[1].set_title("Producción del Mes")

    # Hide x labels and tick labels for top plots and y ticks for right plots.
    for ax in axs.flat:
        ax.label_outer()

    # Save figuro to a temporary buffer.
    buf = BytesIO()
    fig.savefig(buf, format="png")
    # Embed the result in the html output.
    data = base64.b64encode(buf.getbuffer()).decode("ascii")

    return data
