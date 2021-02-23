from flask import (
    Blueprint, request, render_template, redirect, url_for
)
from VicSM.models import add_item, Client, Receipt, format_date
from VicSM.inventory import format_price, add_iva
from VicSM import db

bp = Blueprint('client', __name__, url_prefix='/client')

client_heads = {
    'id': "Id.", 'nombre': 'Nombre', 'direccion': 'Dirección', 'tel': 'Tel.',
    'cambio': 'Tipo de Cambio', 'descripcion': 'Descripción del Proyecto',
    'proyecto': 'Proyecto', 'cotizacion': 'Cotización'
}
receipt_heads = {
    "id": "Id.", "grupo": "Grupo", "cambio": "Tipo de Cambio",
    "cantidades": "Cantidades", "total": "Total",
    "fecha": "Fecha"
}


def get_client(search_term):
    try:
        client_id = int(search_term)
        client = Client.query.get(client_id)
    except ValueError:
        client = None

    if not client:
        client = Client.query.filter_by(nombre=search_term).first()
    if not client:
        client = Client.query.filter_by(tel=search_term).first()
    if not client:
        client = Client.query.filter_by(proyecto=search_term).first()

    return client


clients_heads = {}
for head in client_heads:
    if head != "descripcion" and head != "cambio":
        clients_heads[head] = client_heads[head]


@bp.route('/clients', methods=('GET', 'POST'))
def clients():
    if request.method == 'POST':
        search_term = request.form['search_term']
        client = get_client(search_term)

        if client:
            return redirect(url_for('client.profile', client_id=client.id))

    clients = Client.query.all()

    return render_template(
        'client/clients.html', clients=clients, heads=clients_heads
    )


add_heads = {}
for head in client_heads:
    if head != "id" and head != "fecha":
        add_heads[head] = client_heads[head]


@bp.route('/add_client', methods=('GET', 'POST'))
def add_client():
    if request.method == "POST":
        client = Client(
            nombre=request.form["nombre"],
            direccion=request.form["direccion"],
            tel=request.form["tel"],
            cambio=request.form["cambio"],
            proyecto=request.form["proyecto"],
            descripcion=request.form["descripcion"],
            cotizacion=request.form["cotizacion"]
        )
        add_item(client)

        return redirect(url_for('client.clients'))

    return render_template('client/add_client.html', heads=add_heads)


update_heads = {}
for head in client_heads:
    if head != "id":
        update_heads[head] = client_heads[head]


@bp.route('/<int:client_id>/profile', methods=('GET', 'POST'))
def profile(client_id):
    client = get_client(client_id)
    receipts = Receipt.query.all()

    if request.method == "POST":
        try:
            search_term = request.form["search_term"]
            receipt = Receipt.query.get(search_term)
            if receipt:
                return redirect(
                    url_for('receipt.edit_receipt',
                            client_id=client_id, receipt_id=receipt.id)
                )
        except KeyError:
            pass

        try:
            client.nombre = request.form["nombre"]
            client.direccion = request.form["direccion"]
            client.tel = request.form["tel"]
            client.cambio = request.form["cambio"]
            client.proyecto = request.form["proyecto"]
            client.descripcion = request.form["descripcion"]
            client.cotizacion = request.form["cotizacion"]

            db.session.commit()

            return redirect(url_for('client.clients'))
        except KeyError:
            pass

    return render_template(
        'client/profile.html', client=client, heads=update_heads,
        receipts=receipts, receipt_heads=receipt_heads,
        format_price=format_price, add_iva=add_iva, format_date=format_date
    )


@bp.route('/<int:client_id>/remove_client', methods=('POST',))
def remove_client(client_id):
    client = Client.query.get(client_id)
    db.session.delete(client)
    db.session.commit()

    return redirect(url_for('client.clients'))
