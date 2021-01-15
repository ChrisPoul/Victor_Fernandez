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

        frm_main_body = tk.Frame(
            master=self.window
        )
        frm_main_body.pack(fill=tk.BOTH, expand=True)

        main_body(frm_main_body, products, wanted_names)
        frm_main_body.columnconfigure(len(wanted_names), weight=1)

        for i, product in enumerate(products):
            def delete_product():
                self.remove_product(btn_delete["text"])
                frm_main_body.destroy()
                self.main_body()

            btn_delete = tk.Button(
                master=frm_main_body,
                text=product["name"],
                command=delete_product,
                width=1
            )
            btn_delete.grid(row=i+1, column=len(wanted_names), padx=1, pady=1, sticky="wn")
