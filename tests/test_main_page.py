from .test_vicsm import MyTest


class MainPageTest(MyTest):

    def test_main_page(self):
        response = self.client.get("/")

        assert b"Pagina Principal" in response.data
        self.assertTemplateUsed('main_page/main_page.html')
