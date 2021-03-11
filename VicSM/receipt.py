import os
from datetime import datetime
import json
from operator import attrgetter
from flask import (
    Blueprint, render_template, request, redirect, url_for,
    current_app, flash
)
from VicSM.inventory import get_product, format_price, add_iva
from VicSM.client import get_client, client_heads
from VicSM.models import (
    format_date, add_item, Client,
    Receipt, obj_as_dict, Product
)
from VicSM import db

bp = Blueprint('receipt', __name__, url_prefix='/receipt')

product_heads = {
    "cantidad": "Cant.", "nombre": "Nombre",
    "descripcion": "Descripción", "marca": "Marca",
    "imagen": "Imagen", "precio_venta": "Precio Unidad",
    "mas_iva": "Mas Iva", "total": "Total",
    "eliminar": "Eliminar"
}
middle_heads = {
    "nombre": "Nombre del Cliente ó Razón Social", "tel": "Tel/Fax",
    "cambio": "Tipo de Cambio"
}
last_heads = ["direccion", "nombre", "descripcion"]


@bp.route('/<int:client_id>/new_receipt', methods=('GET', 'POST'))
def new_receipt(client_id):
    client = Client.query.get(client_id)
    autocomplete_client_receipt = get_autocomplete_client_data()

    if request.method == "POST":
        try:
            search_term = request.form['search_term']
            client = get_client(search_term)
        except KeyError:
            pass

    if client:
        receipt = Receipt(client_id=client.id)
        add_item(receipt)

        return redirect(
            url_for('receipt.edit_receipt', receipt_id=receipt.id)
        )

    return render_template(
        'receipt/receipt_search.html',
        autocomplete_client_receipt=autocomplete_client_receipt
    )


@bp.route('/<int:receipt_id>/edit_receipt', methods=('GET', 'POST'))
def edit_receipt(receipt_id):
    current_receipt = CurrentReceipt(receipt_id)

    if request.method == "POST":
        current_receipt.process_changes()

    receipt = current_receipt.receipt
    products = current_receipt.products
    client = current_receipt.client
    aasm_image = current_receipt.aasm_image
    autocomplete_receipt_products = get_autocomplete_product_data(
        receipt.cantidades)
    autocomplete_receipt_groups = get_all_groups()

    return render_template(
        'receipt/receipt.html', product_heads=product_heads,
        client_heads=client_heads, products=products,
        cantidades=receipt.cantidades, totals=receipt.totales,
        format_price=format_price, grupo=receipt.grupo,
        client=client, middle_heads=middle_heads, add_iva=add_iva,
        cambio=receipt.cambio, receipt_id=receipt_id,
        fecha=format_date(receipt.fecha), total=receipt.total,
        aasm_image=aasm_image, last_heads=last_heads,
        autocomplete_receipt_products=autocomplete_receipt_products,
        autocomplete_receipt_groups=autocomplete_receipt_groups
    )


product_done_heads = {}
for head in product_heads:
    if head != "eliminar":
        product_done_heads[head] = product_heads[head]


@bp.route('/<int:receipt_id>/receipt_done')
def receipt_done(receipt_id):
    current_receipt = CurrentReceipt(receipt_id)
    receipt = current_receipt.receipt
    products = current_receipt.products
    client = current_receipt.client
    aasm_image = current_receipt.aasm_image

    return render_template(
        'receipt/receipt_done.html', product_heads=product_done_heads,
        client_heads=client_heads, products=products,
        cantidades=receipt.cantidades, totals=receipt.totales,
        format_price=format_price, grupo=receipt.grupo,
        client=client, middle_heads=middle_heads, add_iva=add_iva,
        cambio=receipt.cambio, receipt_id=receipt_id,
        fecha=format_date(receipt.fecha), total=receipt.total,
        aasm_image=aasm_image, last_heads=last_heads,
    )


@bp.route('/<int:receipt_id>/<string:codigo>/remove_product')
def remove_product(receipt_id, codigo):
    current_receipt = CurrentReceipt(receipt_id)
    current_receipt.remove_product(codigo)

    return redirect(
        url_for('receipt.edit_receipt', receipt_id=receipt_id)
    )


@bp.route('/<int:receipt_id>/delete_receipt')
def delete_receipt(receipt_id):
    receipt = get_receipt(receipt_id)
    for code in receipt.cantidades:
        product = get_product(code)
        if product:
            cantidad = receipt.cantidades[code]
            product.inventario += cantidad
            product.unidades_vendidas -= cantidad
    client = receipt.author
    client.total -= receipt.total
    db.session.delete(receipt)
    db.session.commit()

    return redirect(
        url_for('client.profile', client_id=receipt.client_id)
    )


class CurrentReceipt:

    def __init__(self, receipt_id):
        self.aasm_image = get_aasm_image()
        self.receipt = get_receipt(receipt_id)
        self.cantidades = obj_as_dict(self.receipt.cantidades)
        self.cant_ref = obj_as_dict(self.receipt.cant_ref)
        self.totales = obj_as_dict(self.receipt.totales)
        self.client = get_client(self.receipt.client_id)
        if not self.receipt.cambio:
            self.receipt.cambio = self.client.cambio
        self.receipt.fecha = datetime.now()
        self.update_receipt_products()
        self.error = None

    def process_changes(self):
        try:
            self.receipt.grupo = request.form['grupo']
        except KeyError:
            pass
        try:
            cambio = request.form['cambio']
            self.update_cambio(cambio)
        except KeyError:
            pass

        self.update_cantidades_and_totales()
        self.update_receipt()

    def update_cambio(self, cambio):
        try:
            cambio = float(cambio)
        except ValueError:
            cambio = self.client.cambio
        self.receipt.cambio = cambio

    def update_cantidades_and_totales(self):
        for code in self.products:
            try:
                self.update_cantidades_cantidad(code)
                self.update_totales_total(code)
            except KeyError:
                pass

        if self.cantidades != self.cant_ref:
            self.handle_change_in_cantidades()

        self.cant_ref = self.cantidades

    def update_cantidades_cantidad(self, code):
        cantidad = request.form[code]
        try:
            cantidad = int(cantidad)
        except ValueError:
            cantidad = 0
        self.cantidades[code] = cantidad

    def update_totales_total(self, code):
        product = self.products[code]
        precio_venta = product.precio_venta
        total = self.cantidades[code] * precio_venta * 1.16
        self.totales[code] = total

    def handle_change_in_cantidades(self):
        for code in self.cantidades:
            product = self.update_product_sales(code)
            if product.inventario < 0:
                self.handle_inv_exceeded(product)

    def update_product_sales(self, code):
        product = get_product(code)
        change = self.get_change_in_cantidades(code)
        product.unidades_vendidas += change
        product.inventario -= change

        return product

    def get_change_in_cantidades(self, code):
        new_cantidad = self.cantidades[code]
        try:
            previous_cantidad = self.cant_ref[code]
        except KeyError:
            self.cant_ref[code] = 0
            previous_cantidad = 0
        change = new_cantidad - previous_cantidad

        return change

    def handle_inv_exceeded(self, product):
        cantidad = self.cantidades[product.codigo]
        inv_disponible = product.inventario + cantidad
        exedent = product.inventario * -1
        if exedent == 1:
            unidades_txt = "unidad"
        else:
            unidades_txt = "unidades"

        self.error = f"""
            Inventario exedido por {exedent} {unidades_txt}, solo hay
            {inv_disponible} unidades de {product.nombre} disponibles
        """

    def update_receipt(self):
        self.update_client_total()
        self.add_product()
        self.update_receipt_products()
        self.receipt.cantidades = self.cantidades
        self.receipt.cant_ref = self.cant_ref
        self.receipt.totales = self.totales
        self.receipt.total = get_total(self.totales)
        if self.error:
            flash(self.error)
        else:
            db.session.commit()

    def update_client_total(self):
        receipt_total_before_updating = self.receipt.total
        receipt_total_after_updating = get_total(self.totales)
        total_change = receipt_total_before_updating - receipt_total_after_updating
        self.client.total -= total_change

    def add_product(self):
        try:
            codigo = request.form["product_search_term"]
        except KeyError:
            codigo = ""
        product = get_product(codigo)
        if product is not None:
            self.cantidades[product.codigo] = 0
            self.totales[product.codigo] = 0

    def update_receipt_products(self):
        self.products = {}
        codigos = []
        for code in self.cantidades:
            codigos.append(code)

        for code in codigos[::-1]:
            product = get_product(code)
            if product is not None:
                self.products[code] = product
            else:
                self.cantidades.pop(code)
                self.receipt.cantidades = self.cantidades
                self.totales.pop(code)
                self.receipt.totales = self.totales

        filler = 6 - len(self.products)
        if filler > 0:
            for i in range(filler):
                self.products[i] = DummyProduct()

    def remove_product(self, code):
        product = get_product(code)
        cantidad = self.cantidades[code]
        product.inventario += cantidad
        product.unidades_vendidas -= cantidad

        self.cantidades.pop(code)
        self.totales.pop(code)
        self.update_receipt()


class DummyProduct:
    def __init__(self):
        self.grupo = ""
        self.serie = ""
        self.codigo = ""
        self.nombre = ""
        self.descripcion = ""
        self.marca = ""
        self.imagen = "white_background.jpg"
        self.mi_precio = 0
        self.precio_venta = 0
        self.inventario = 0


def get_receipt(receipt_id):
    receipt = Receipt.query.get(receipt_id)

    return receipt


def get_total(totals):
    total = 0
    for key in totals:
        total += totals[key]

    return round(total, 2)


def get_aasm_image():
    references_path = os.path.join(
        current_app.static_folder, 'references.json')
    with open(references_path) as aasm_reference_file:
        aasm_reference = json.load(aasm_reference_file)
    aasm_image = aasm_reference["aasm"]

    return aasm_image


def get_all_groups():
    receipts = Receipt.query.all()
    groups = []
    for receipt in receipts:
        if receipt.grupo not in groups:
            groups.append(receipt.grupo)

    return groups


def get_autocomplete_client_data():
    clients = Client.query.all()
    clients = sorted(clients, key=attrgetter('id'), reverse=True)
    autocomplete_clients = [client.nombre for client in clients]

    return autocomplete_clients


def get_autocomplete_product_data(cantidades):
    products = Product.query.all()
    autocomplete_products = []
    for product in products:
        if product.codigo not in cantidades:
            autocomplete_products.append(product.nombre)
            autocomplete_products.append(product.codigo)

    return autocomplete_products
