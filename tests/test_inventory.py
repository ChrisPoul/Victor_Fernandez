from .test_vicsm import MyTest


class InventoryTests(MyTest):

    def test_inv_page(self):
        response = self.client.get('/inventory')

        assert b"Inventario" in response.data
