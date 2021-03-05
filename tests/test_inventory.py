from .test_vicsm import MyTest
from VicSM.models import Product, add_item


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

        self.assertTemplateUsed("inventory/inventory.html")
        assert b"Inventario" in response.data
        assert b"test nombre" in response.data
