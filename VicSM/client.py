from flask import (
    Blueprint, request, render_template, flash, redirect, url_for
)
from VicSM.db import get_db

bp = Blueprint('client', __name__, url_prefix='/client')

heads = ['nombre', 'direccion', 'id', 'tel', 
    'fecha', 'moneda', 'proyecto', 'descripcion',
    'cotizacion'
]


def get_client(client_id):
    pass


@bp.route('/clients')
def clients():
    db = get_db()
    clients = db.execute(
        'SELECT c.id, nombre, direccion, tel, fecha,'
        ' moneda, proyecto, descripcion, cotizacion'
        ' FROM client c'
    ).fetchall()

    return render_template('client/clients.html', clients=clients, heads=heads)


@bp.route('/add_client', methods=('GET', 'POST'))
def add_client():
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

    return render_template('client/add_client.html', heads=heads)


@bp.route('/profile')
def profile():

    return render_template('client/profile.html')
