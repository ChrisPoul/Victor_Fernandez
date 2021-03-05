import math
import base64
import os
from io import BytesIO
from flask import (
    Blueprint, render_template, request,
    redirect, url_for, current_app
)
from operator import attrgetter
from datetime import datetime
from matplotlib.figure import Figure
from VicSM.models import (
    Product, Client, format_date, days,
    get_references, save_references
)
from VicSM.inventory import add_iva, format_price


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
    total_earnings = get_current_total_earnings()
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
        format_price=format_price,
        format_time=format_time,
        product_heads=product_heads,
        total_earnings=total_earnings
    )


@bp.route('/site_config', methods=('GET', 'POST'))
def site_config():
    if request.method == 'POST':
        receipt_image = request.files["image_receipt"]
        if receipt_image:
            save_my_image("aasm", receipt_image)
            return redirect(url_for('receipt.new_receipt', client_id=0))

        site_icon = request.files["image_icon"]
        if site_icon:
            site_icon.filename = "app_icon.ico"
            save_my_image("site_icon", site_icon)
            return redirect(url_for('main_page.main_page'))

    return render_template('main_page/site_config.html')


def save_my_image(key, image_file):
    references = get_references()
    image_name = references[key]
    images_path = os.path.join(current_app.static_folder, "my_images")
    image_path = os.path.join(images_path, image_name)
    try:
        os.remove(image_path)
    except FileNotFoundError:
        pass

    image_name = image_file.filename
    references[key] = image_name
    image_path = os.path.join(images_path, image_name)
    image_file.save(image_path)
    save_references(references)


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


class Others:

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
    ms_products.append(Others(others_unidades_vendidas))

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
    if units_sold[-1] == 0:
        products_sold = products_sold[:-1]
        units_sold = units_sold[:-1]
    ax.pie(units_sold, labels=products_sold)
    ax.set_title('Productos Vendidos')

    buf = BytesIO()
    fig.savefig(buf, format="png")
    data = base64.b64encode(buf.getbuffer()).decode("ascii")

    return data


def get_current_total_earnings():
    clients = Client.query.all()
    ventas = 0
    for client in clients:
        ventas += client.total * 1.16

    products = Product.query.all()
    costos = 0
    for product in products:
        costos += product.mi_precio * product.unidades_vendidas

    utilidades = ventas - costos

    ganancias_totales = {
        "ventas": ventas,
        "utilidades": utilidades
    }

    return ganancias_totales


def get_total_earnings():
    references = get_references()
    current_total_earnings = get_current_total_earnings()
    total_earnings = {}
    for key in current_total_earnings:
        if references[key][-1] != current_total_earnings[key]:
            references[key].append(current_total_earnings[key])
        total_earnings[key] = references[key]
    save_references(references)

    return total_earnings


def get_summary_figure():
    fig = Figure(dpi=220)
    ax = fig.subplots()
    total_earnings = get_total_earnings()
    ventas = total_earnings["ventas"]
    utilidades = total_earnings["utilidades"]

    ax.plot(ventas, label="Ventas")
    ax.plot(utilidades, label="Utilidades")
    ax.legend()
    ax.set_title("Ganancias a través del tiempo")

    # Save figuro to a temporary buffer.
    buf = BytesIO()
    fig.savefig(buf, format="png")
    # Embed the result in the html output.
    data = base64.b64encode(buf.getbuffer()).decode("ascii")

    return data
