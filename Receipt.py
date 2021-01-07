import tkinter as tk
from Functions import format_price, add_iva, get_product_total, first_row, add_totals, convert_to_pesos



class Receipt:

    def __init__(self):
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


    def main_body(self, frm_body, products):
        wanted_names = {}
        for key in self.wanted_names:
            if key != "amnt." and key != "Total":
                wanted_names[key] = self.wanted_names[key]

        first_row(frm_body, wanted_names)

        def get_total():
            user_input = ent_amnt.get()
            amnt = int(user_input)
            total = get_product_total(product, amnt)
            lbl_value["text"] = add_iva(total)


        for i, product in enumerate(products):
            frm_body.rowconfigure(i+1, weight=1, minsize=50)

            for j, key in enumerate(wanted_names):
                frm_body.columnconfigure(j, weight=1, minsize=50)
                value = product[key]
                my_wrap_length = 400
                my_justify = "left"

                if key == "my_price" or key == "sell_price":
                    value = format_price(value)

                elif key == "brand":
                    my_wrap_length = 60
                    my_justify = "center"

                frm_value = tk.Frame(
                    master=frm_body,
                    relief=tk.SUNKEN,
                    height=4,
                    borderwidth=1
                )
                frm_value.grid(row=i+1, column=j, padx=2, pady=2, sticky="nsew")

                lbl_value = tk.Label(
                    master=frm_value,
                    text=value,
                    relief=tk.GROOVE,
                    wraplength=my_wrap_length,
                    justify=my_justify,
                    height=3
                )
                lbl_value.pack(fill=tk.BOTH, expand=True, padx=1, pady=1)


    def totals_body(self, frm_totals_body, products):

        wanted_names = {}
        for key in self.wanted_names:
            if key == "amnt." or key == "Total":
                wanted_names[key] = self.wanted_names[key]

        first_row(frm_totals_body, wanted_names)


        self.amnts = []
        self.lbl_totals = []
        for i, product in enumerate(products):
            frm_totals_body.rowconfigure(i+1, weight=1, minsize=50)

            for key in wanted_names:
                product[key] = 0

            for j, key in enumerate(wanted_names):
                frm_totals_body.columnconfigure(j, weight=1, minsize=50)
                value = product[key]

                frm_value = tk.Frame(
                master=frm_totals_body,
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



    def submit(self, frm_submit, products):
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
