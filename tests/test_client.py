from .test_vicsm import MyTest
from VicSM.models import Client, add_item
from VicSM.client import get_client


class ClientTests(MyTest):

    def test_clients_page(self):
        response = self.client.get('/clients')

        assert b"Clientes" in response.data
        self.assertTemplateUsed('client/clients.html')
        self.assert200(response)

    def test_client_profile(self):
        client = Client(
            nombre="Test",
            direccion="test direccion",
            tel="123 456 7890",
            cambio=1,
            proyecto="test proyect",
            descripcion="test descripcion",
            cotizacion="test cotizacion"
        )
        add_item(client)
        response = self.client.get('/1/profile')

        assert b"Test" in response.data
        assert b"test direccion" in response.data
        assert b"123 456 7890" in response.data
        assert b"test proyect" in response.data
        assert b"test descripcion" in response.data
        assert b"test cotizacion" in response.data
        self.assertTemplateUsed('client/profile.html')
        self.assert200(response)

    def test_get_client(self):
        client = get_client("Test")
        assert client is None

        test_client = Client(
            nombre="Test",
            direccion="test direccion",
            tel="123 456 7890",
            cambio=1,
            proyecto="test proyect",
            descripcion="test descripcion",
            cotizacion="test cotizacion"
        )
        add_item(test_client)
        client = get_client("Test")
        assert client.tel == "123 456 7890"
