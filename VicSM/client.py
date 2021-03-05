from flask import (
    Blueprint, request, render_template, redirect,
    url_for, flash
)
from operator import attrgetter
from VicSM.models import add_item, Client, Receipt, format_date
from VicSM.inventory import format_price, add_iva
from VicSM import db

bp = Blueprint('client', __name__)

client_heads = {
    'id': "Id.", 'nombre': 'Nombre',
    'direccion': 'Dirección', 'tel': 'Tel.',
    'cambio': 'Tipo de Cambio',
    'descripcion': 'Descripción del Proyecto',
    'proyecto': 'Proyecto',
    'cotizacion': 'Cotización'
}
receipt_heads = {
    "id": "Id.", "grupo": "Grupo",
    "cambio": "Tipo de Cambio",
    "productos": "Productos",
    "cantidades": "Cantidades",
    "total": "Total",
    "fecha": "Fecha"
}


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
    clients = sorted(clients, key=attrgetter('id'), reverse=True)

    return render_template(
        'client/clients.html', clients=clients, heads=clients_heads
    )


add_heads = {}
for head in client_heads:
    if head != "id":
        add_heads[head] = client_heads[head]


@bp.route('/add_client', methods=('GET', 'POST'))
def add_client():
    form_values = {}
    for key in add_heads:
        form_values[key] = ""

    if request.method == "POST":
        for key in form_values:
            form_values[key] = request.form[key]
        error = None
        try:
            float(form_values['cambio'])
        except ValueError:
            error = "Introdujo un número invalido"

        if not error:
            client = Client(
                nombre=form_values["nombre"],
                direccion=form_values["direccion"],
                tel=form_values["tel"],
                cambio=form_values["cambio"],
                proyecto=form_values["proyecto"],
                descripcion=form_values["descripcion"],
                cotizacion=form_values["cotizacion"]
            )
            error = add_item(client)

            if not error:
                return redirect(url_for('client.clients'))

        flash(error)

    return render_template(
        'client/add_client.html', heads=add_heads,
        form_values=form_values
    )


def get_client_receipts(client_id):
    receipts = Receipt.query.filter_by(client_id=client_id).all()
    client_receipts = {}
    for i, receipt in enumerate(receipts, start=1):
        client_receipts[i] = receipt
    return client_receipts


@bp.route('/<int:client_id>/profile', methods=('GET', 'POST'))
def profile(client_id):
    client = get_client(client_id)
    client_receipts = get_client_receipts(client_id)

    if request.method == "POST":
        try:
            search_term = request.form["search_term"]
            try:
                search_term = int(search_term)
            except ValueError:
                pass
            receipt = client_receipts[search_term]
            if receipt:
                return redirect(
                    url_for('receipt.edit_receipt', receipt_id=receipt.id)
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
            error = None

            try:
                float(client.cambio)
            except ValueError:
                error = "Introdujo un número invalido"

            if not error:
                db.session.commit()
                return redirect(url_for('client.clients'))

            flash(error)

        except KeyError:
            pass

    return render_template(
        'client/profile.html', format_price=format_price,
        receipts=client_receipts, receipt_heads=receipt_heads,
        add_iva=add_iva, format_date=format_date,
        client=client, heads=add_heads
    )


@bp.route('/<int:client_id>/remove_client', methods=('POST',))
def remove_client(client_id):
    client = Client.query.get(client_id)
    db.session.delete(client)
    db.session.commit()

    return redirect(url_for('client.clients'))


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
