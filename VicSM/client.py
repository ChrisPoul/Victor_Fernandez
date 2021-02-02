from flask import (
    Blueprint, request, render_template, flash, redirect, url_for
)
from VicSM.db import get_db

bp = Blueprint('client', __name__, url_prefix='/client')

client_heads = {'nombre': 'Nombre', 'direccion': 'Dirección', 'tel': 'Tel.', 
    'fecha': 'Fecha', 'moneda': 'Cambio', 'proyecto': 'Nombre Proyecto',
    'descripcion': 'Descripción', 'cotizacion': 'Cotización'
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
    add_heads = [head for head in client_heads if head != "id" and head != "fecha"]

    if request.method == "POST":
        nombre = request.form["nombre"]
        direccion = request.form["direccion"]
        tel = request.form["tel"]
        moneda = request.form["moneda"]
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
                ' moneda, proyecto, descripcion, cotizacion)'
                ' VALUES (?, ?, ?, ?, ?, ?, ?)', (nombre, direccion,
                tel, moneda, proyecto, descripcion, cotizacion)
            )
            db.commit()

            return redirect(url_for('client.clients'))

    return render_template('client/add_client.html', heads=add_heads)


def get_client(client_id):
    db = get_db()
    client = db.execute(
        'SELECT * FROM client WHERE id = ?', (client_id,)
    ).fetchone()

    return client


@bp.route('/<int:client_id>/profile', methods=('GET', 'POST'))
def profile(client_id):
    client = get_client (client_id)
    update_heads = [head for head in client_heads if head != "id"]

    if request.method == "POST":
        nombre = request.form["nombre"]
        direccion = request.form["direccion"]
        tel = request.form["tel"]
        moneda = request.form["moneda"]
        proyecto = request.form["proyecto"]
        descripcion = request.form["descripcion"]
        cotizacion = request.form["cotizacion"]

        db = get_db()
        db.execute(
            'UPDATE client SET nombre = ?, direccion = ?, tel = ?,'
            ' moneda = ?, proyecto = ?, descripcion = ?, cotizacion = ?'
            ' WHERE id = ?', (nombre, direccion, tel, moneda, proyecto,
            descripcion, cotizacion, client_id)
        )
        db.commit()

        return redirect(url_for('client.clients'))

    return render_template('client/profile.html', client=client, heads=update_heads)


@bp.route('/<int:client_id>/remove_client', methods=('POST',))
def remove_client(client_id):
    db = get_db()
    db.execute(
        'DELETE FROM client WHERE id = ?', (client_id,)
    )
    db.commit()

    return redirect(url_for('client.clients'))
