from .test_vicsm import MyTest
from VicSM.models import Product, add_item
from VicSM.inventory import (
    format_price, add_iva, get_products, get_product
)


class InventoryTests(MyTest):

    def test_inv_page(self):
        product = Product(
            grupo="test grupo",
            serie="test serie",
            codigo="test codigo",
            nombre="test nombre",
            descripcion="test",
            marca="test",
            imagen="test.jpg",
            mi_precio=0,
            precio_venta=0,
            inventario=0
        )
        add_item(product)
        response = self.client.get('/inventory')

        assert b"Inventario" in response.data
        assert b"test nombre" in response.data
        self.assertTemplateUsed("inventory/inventory.html")
        self.assert200(response)

    def test_format_price(self):
        assert format_price(0) == "$0.00"
        assert format_price(10) == "$10.00"
        assert format_price(22.1) == "$22.10"
        assert format_price(1000) == "$1,000.00"
        assert format_price(50_000_000) == "$50,000,000.00"

    def test_add_iva(self):
        assert add_iva(1) == "$1.16"

    def test_get_products(self):
        product1 = Product(
            grupo="test grupo",
            serie="test serie",
            codigo="test codigo",
            nombre="test nombre",
            descripcion="test",
            marca="test",
            imagen="test.jpg",
            mi_precio=0,
            precio_venta=0,
            inventario=0
        )
        add_item(product1)
        product2 = Product(
            grupo="test grupo",
            serie="test serie",
            codigo="test codigo2",
            nombre="test nombre2",
            descripcion="test",
            marca="test",
            imagen="test2.jpg",
            mi_precio=0,
            precio_venta=0,
            inventario=0
        )
        add_item(product2)
        products = get_products()

        assert product1 in products
        assert product2 in products

    def test_get_product(self):
        product = get_product("test nombre")
        assert product is None

        test_product = Product(
            grupo="test grupo",
            serie="test serie",
            codigo="test codigo",
            nombre="test nombre",
            descripcion="test",
            marca="test",
            imagen="test.jpg",
            mi_precio=0,
            precio_venta=0,
            inventario=0
        )
        add_item(test_product)
        product = get_product("test codigo")
        assert product.nombre == "test nombre"
