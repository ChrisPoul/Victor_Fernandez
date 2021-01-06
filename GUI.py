import tkinter as tk
from Product_Catalog import Product_Catalog
from Functions import format_price, add_iva

product_catalog = Product_Catalog()

window = tk.Tk()

spanish_keys = ["Codigo", "Nombre", "Descripción", "Marca", "Imagen", "Mi precio", "Mi precio mas iva", "Precio de Venta", "Precio Venta mas iva", "amnt.", "Total"]

for i, key in enumerate(spanish_keys):
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
        text=key,
        height=2
    )
    key_lbl.pack(fill=tk.X, expand=True, side=tk.BOTTOM)

for i, product in enumerate(product_catalog.products_list):
    product["amnt."] = 0
    product["Total"] = 0

    window.rowconfigure(i+1, weight=1, minsize=50)

    for j, key in enumerate(product):
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

        lbl_value = tk.Label(
            master=frm_value,
            text=value,
            relief=tk.GROOVE,
            wraplength=my_wrap_length,
            justify=my_justify,
            height=3
        )
        lbl_value.pack(fill=tk.BOTH, expand=True, padx=1, pady=1)


window.mainloop()
