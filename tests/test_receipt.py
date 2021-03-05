from .test_vicsm import MyTest
from VicSM.models import Client, Receipt, add_item
from datetime import datetime


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
