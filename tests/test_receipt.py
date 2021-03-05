from datetime import datetime
from .test_vicsm import MyTest
from VicSM.models import Client, Receipt, add_item
from VicSM.receipt import (
    get_total, get_aasm_image, get_receipt_products,
    get_receipt
)


class ReceiptTests(MyTest):

    def test_new_receipt(self):
        response = self.client.get('receipt/0/new_receipt')

        assert b"Recibo Nuevo" in response.data
        self.assertTemplateUsed('receipt/receipt_search.html')
        self.assert200(response)

    def test_edit_receipt(self):
        client = Client(
            nombre="Test client",
            direccion="test direccion",
            tel="123 456 7890",
            cambio=1,
            proyecto="test proyect",
            descripcion="test descripcion",
            cotizacion="test cotizacion"
        )
        add_item(client)
        receipt = Receipt(
            grupo="test receipt",
            cambio=1,
            totales={"TEST": 10},
            total=10,
            cantidades={"TEST": 1},
            cant_ref={"TEST": 1},
            fecha=datetime.now(),
            client_id=1
        )
        add_item(receipt)
        response = self.client.get('receipt/1/edit_receipt')

        assert b"test receipt" in response.data
        assert b"Test client" in response.data
        self.assertTemplateUsed('receipt/receipt.html')
        self.assert200(response)

    def test_get_total(self):
        assert get_total({}) == 0
        assert get_total({"a": 1}) == 1
        assert get_total({"a": 10, "b": 40})

    def test_get_aasm_image(self):
        aasm_image = get_aasm_image()
        assert aasm_image is not None
        assert type(aasm_image) is str

    def test_get_receipt_products(self):
        client = Client(
            nombre="Test client",
            direccion="test direccion",
            tel="123 456 7890",
            cambio=1,
            proyecto="test proyect",
            descripcion="test descripcion",
            cotizacion="test cotizacion"
        )
        add_item(client)
        receipt = Receipt(
            client_id=1,
            cantidades={},
            totales={}
        )
        receipt_products = get_receipt_products(receipt)

        assert len(receipt_products) == 6

    def test_get_receipt(self):
        client = Client(
            nombre="Test client",
            direccion="test direccion",
            tel="123 456 7890",
            cambio=1,
            proyecto="test proyect",
            descripcion="test descripcion",
            cotizacion="test cotizacion"
        )
        add_item(client)
        receipt = Receipt(client_id=1)
        add_item(receipt)

        assert get_receipt(1) is not None
        assert get_receipt(2) is None
