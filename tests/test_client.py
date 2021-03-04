from .test_vicsm import MyTest


class ClientTests(MyTest):

    def test_clients_page(self):
        response = self.client.get('/client/clients')

        assert b"Clientes" in response.data
