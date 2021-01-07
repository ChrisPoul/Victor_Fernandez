import tkinter as tk
from Product_Catalog import Product_Catalog
from Functions import main_body

class Inventory_GUI(Product_Catalog):

    def __init__(self, window):
        Product_Catalog.__init__(self)
        self.wanted_names = {
        "code": "Codigo",
        "name": "Nombre",
        "description": "Descripción",
        "brand": "Marca",
        "image": "Imagen",
        "my_price": "Mi precio",
        "my_price_iva": "Mi precio mas iva",
        "sell_price": "Precio de Venta",
        "sell_price_iva": "Precio Venta mas iva"
        }
        self.window = window

        self.main_body()


    def main_body(self):
        wanted_names = self.wanted_names
        products = self.products_list

        main_body(self.window, products, wanted_names)