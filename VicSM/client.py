from flask import (
    Blueprint, request, render_template, flash, redirect, url_for
)
from VicSM.db import get_db, get_receipts

bp = Blueprint('client', __name__, url_prefix='/client')

client_heads = {
    'id': "Id.", 'nombre': 'Nombre', 'direccion': 'Dirección', 'tel': 'Tel.', 
    'fecha': 'Fecha', 'cambio': 'Tipo de Cambio', 'proyecto': 'Proyecto',
    'descripcion': 'Descripción del Proyecto', 'cotizacion': 'Cotización'
    }


@bp.route('/clients')
def clients():
    db = get_db()
    clients = db.execute(
        'SELECT * FROM client'
    ).fetchall()

    return render_template('client/clients.html', clients=clients, heads=client_heads)


@bp.route('/add_client', methods=('GET', 'POST'))
def add_client():
    add_heads = {}
    for head in client_heads:
        if head != "id" and head != "fecha":
            add_heads[head] = client_heads[head]

    if request.method == "POST":
        nombre = request.form["nombre"]
        direccion = request.form["direccion"]
        tel = request.form["tel"]
        cambio = request.form["cambio"]
        proyecto = request.form["proyecto"]
        descripcion = request.form["descripcion"]
        cotizacion = request.form["cotizacion"]

        error = None

        if not nombre or not proyecto:
            error = "Nombre and Proyecto needed"

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO client (nombre, direccion, tel,'
                ' cambio, proyecto, descripcion, cotizacion)'
                ' VALUES (?, ?, ?, ?, ?, ?, ?)', (nombre, direccion,
                tel, cambio, proyecto, descripcion, cotizacion)
            )
            db.commit()

            return redirect(url_for('client.clients'))

    return render_template('client/add_client.html', heads=add_heads)


def get_client(search_term):
    db = get_db()
    for head in client_heads:
        client = db.execute(
            f'SELECT * FROM client WHERE {head} = ?', (search_term,)
        ).fetchone()

        if client is not None:
            return client

    return client


def search_receipt_id(client_id, search_term):
    receipts = get_receipts()
    client_receipts = receipts[str(client_id)]
    
    try:
        dummy_var = client_receipts[search_term]
        return True
    except KeyError:
        return False


@bp.route('/<int:client_id>/profile', methods=('GET', 'POST'))
def profile(client_id):
    client = get_client(client_id)
    receipts = get_receipts()
    client_receipts = receipts[str(client_id)]
    update_heads = {}
    for head in client_heads:
        if head != "id":
            update_heads[head] = client_heads[head]

    if request.method == "POST":
        try:
            search_term = request.form["search_term"]
            if search_receipt_id(client_id, search_term):
                return redirect(
                    url_for('receipt.edit_receipt', client_id=client_id, receipt_id=search_term)
                    )
        except KeyError:
            pass

        try:
            nombre = request.form["nombre"]
            direccion = request.form["direccion"]
            tel = request.form["tel"]
            cambio = request.form["cambio"]
            proyecto = request.form["proyecto"]
            descripcion = request.form["descripcion"]
            cotizacion = request.form["cotizacion"]

            db = get_db()
            db.execute(
                'UPDATE client SET nombre = ?, direccion = ?, tel = ?,'
                ' cambio = ?, proyecto = ?, descripcion = ?, cotizacion = ?'
                ' WHERE id = ?', (nombre, direccion, tel, cambio, proyecto,
                descripcion, cotizacion, client_id)
            )
            db.commit()

            return redirect(url_for('client.clients'))
        except KeyError:
            pass

    return render_template(
        'client/profile.html', client=client, heads=update_heads, receipts=client_receipts
        )


@bp.route('/<int:client_id>/remove_client', methods=('POST',))
def remove_client(client_id):
    db = get_db()
    db.execute(
        'DELETE FROM client WHERE id = ?', (client_id,)
    )
    db.commit()

    return redirect(url_for('client.clients'))
