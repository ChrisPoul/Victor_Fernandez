from .test_vicsm import MyTest
from VicSM import db
from VicSM.models import (
    Product, Client, Receipt, add_item
)


class DbTests(MyTest):

    def test_add_product(self):
        product = Product(
            grupo="test",
            serie="test",
            codigo="test",
            nombre="test",
            descripcion="test",
            marca="test",
            imagen="test",
            mi_precio=0,
            precio_venta=0,
            inventario=0,
            inv_ref=0,
            unidades_vendidas=0
        )
        error = add_item(product)

        assert error is None
        assert product in db.session

    def test_add_client(self):
        client = Client(
            nombre="test",
            direccion="test",
            tel="test",
            cambio=1,
            proyecto="test",
            descripcion="test",
            cotizacion="test"
        )
        error = add_item(client)

        assert error is None
        assert client in db.session

    def test_add_receipt(self):
        receipt = Receipt(client_id=1)
        error = add_item(receipt)

        assert error is None
        assert receipt in db.session

    def test_add_repeated_item(self):
        item1 = Client(
            nombre="test",
            direccion="test",
            tel="test",
            cambio=1,
            proyecto="test",
            descripcion="test",
            cotizacion="test"
        )
        error1 = add_item(item1)
        item2 = Client(
            nombre="test",
            direccion="test",
            tel="test",
            cambio=1,
            proyecto="test",
            descripcion="test",
            cotizacion="test"
        )
        error2 = add_item(item2)

        assert error1 is None
        assert item1 in db.session
        assert error2 == "Error, uno de los valores que introdujo ya se encuentra en uso"
