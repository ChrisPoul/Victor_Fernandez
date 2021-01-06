import tkinter as tk
from Functions import format_price, add_iva, get_product_total



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


    def first_row(self, window):
        for i, key in enumerate(self.wanted_names):
            window.rowconfigure(0, weight=1, minsize=50)
            window.columnconfigure(i, weight=1, minsize=50)

            key_frame = tk.Frame(
                master=window,
                relief=tk.RAISED,
                borderwidth=1
            )
            key_frame.grid(row=0, column=i, padx=2, pady=5, sticky="ews")

            key_lbl = tk.Label(
                master=key_frame,
                text=self.wanted_names[key],
                height=2
            )
            key_lbl.pack(fill=tk.X, expand=True, side=tk.BOTTOM)


    def body(self, window, products):
        def get_total():
            user_input = ent_amnt.get()
            amnt = int(user_input)
            total = get_product_total(product, amnt)
            lbl_value["text"] = add_iva(total)


        for i, product in enumerate(products):
            product["amnt."] = 0
            product["Total"] = 0
            window.rowconfigure(i+1, weight=1, minsize=50)

            for j, key in enumerate(self.wanted_names):
                window.columnconfigure(j, weight=1, minsize=50)
                value = product[key]
                my_wrap_length = 400
                my_justify = "left"

                if key == "my_price" or key == "sell_price":
                    value = format_price(value)

                elif key == "brand":
                    my_wrap_length = 60
                    my_justify = "center"

                frm_value = tk.Frame(
                    master=window,
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

                else:
                    if key == "Total":
                        btn_total = tk.Button(
                            master=frm_value,
                            text="=",
                            command=get_total
                        )
                        btn_total.pack(side=tk.LEFT)

                    lbl_value = tk.Label(
                        master=frm_value,
                        text=value,
                        relief=tk.GROOVE,
                        wraplength=my_wrap_length,
                        justify=my_justify,
                        height=3
                    )
                    lbl_value.pack(fill=tk.BOTH, expand=True, padx=1, pady=1)
