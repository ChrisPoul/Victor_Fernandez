import tkinter as tk
from Product_Catalog import Product_Catalog
from Functions import format_price, add_iva, get_product_total, top_row, add_totals, convert_to_pesos
from Functions import main_body

class Receipt_GUI(Product_Catalog):

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
        "sell_price_iva": "Precio Venta mas iva",
        "amnt.": "Cantidad",
        "Total": "Total"
        }

        self.window = window
        self.frm_body = tk.Frame(
            master=window
        )
        self.frm_body.pack(fill=tk.BOTH, expand=True)

        self.main_body()
        self.totals_body()
        self.submit_body()


    def main_body(self):
        products = self.products_list

        wanted_names = {}
        for key in self.wanted_names:
            if key != "amnt." and key != "Total":
                wanted_names[key] = self.wanted_names[key]

        frm_main = tk.Frame(
            master=self.frm_body
        )
        frm_main.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)

        main_body(frm_main, products, wanted_names)


    def totals_body(self):
        products = self.products_list

        wanted_names = {}
        for key in self.wanted_names:
            if key == "amnt." or key == "Total":
                wanted_names[key] = self.wanted_names[key]

        frm_totals = tk.Frame(
            master=self.frm_body
        )
        frm_totals.pack(fill=tk.BOTH, expand=True, side=tk.RIGHT)

        top_row(frm_totals, wanted_names)

        self.amnts = []
        self.lbl_totals = []
        for i, product in enumerate(products):
            frm_totals.rowconfigure(i+1, weight=1, minsize=50)

            for key in wanted_names:
                product[key] = 0

            for j, key in enumerate(wanted_names):
                frm_totals.columnconfigure(j, weight=1, minsize=50)
                value = product[key]

                frm_value = tk.Frame(
                master=frm_totals,
                relief=tk.SUNKEN,
                height=4,
                borderwidth=1
                )
                frm_value.grid(row=i+1, column=j, padx=2, pady=2, sticky="nsew")

                if key == "amnt.":
                    ent_amnt = tk.Entry(
                        master=frm_value,
                        justify="center",
                        width=5
                    )
                    ent_amnt.pack(fill=tk.BOTH, expand=True, padx=1, pady=1)
                    self.amnts.append(ent_amnt)

                elif key == "Total":
                    value = format_price(value)
                    lbl_value = tk.Label(
                        master=frm_value,
                        text=value,
                        relief=tk.GROOVE,
                        height=3
                    )
                    lbl_value.pack(fill=tk.BOTH, expand=True, padx=1, pady=1)
                    self.lbl_totals.append(lbl_value)



    def submit_body(self):
        window = self.window
        products = self.products_list

        self.total = 0
        def get_totals():
            totals = [0]
            for i, amnt in enumerate(self.amnts):
                try:
                    cuantity = int(amnt.get())
                    product_total = get_product_total(products[i], cuantity)
                    products[i]["Total"] = product_total
                    totals.append(product_total)
                    self.lbl_totals[i]["text"] = add_iva(product_total)

                except ValueError:
                    pass

            self.total = add_totals(totals)
            lbl_total_dollars["text"] = add_iva(self.total)

            total_pesos = add_iva(convert_to_pesos(self.total))
            lbl_total_pesos["text"] = total_pesos

        frm_submit = tk.Frame(
            master=window,
            height=2
        )
        frm_submit.pack(fill=tk.X)

        lbl_total_dollars = tk.Label(
            master=frm_submit,
            text=format_price(self.total),
            relief=tk.RAISED,
            borderwidth=2,
            height=2
        )
        lbl_total_dollars.pack(side=tk.RIGHT, padx=5, pady=5)

        lbl_total_pesos = tk.Label(
            master=frm_submit,
            text=f"Pesos Mexicanos: {format_price(self.total)}",
            relief=tk.RAISED,
            borderwidth=2,
            height=2
        )
        lbl_total_pesos.pack(side=tk.RIGHT, padx=5, pady=5)

        btn_submit = tk.Button(
            master=frm_submit,
            text="Get Total",
            relief=tk.RAISED,
            borderwidth=2,
            height=2,
            command=get_totals
        )
        btn_submit.pack(side=tk.RIGHT)