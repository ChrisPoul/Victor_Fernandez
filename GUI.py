import tkinter as tk
from Product_Catalog import Product_Catalog

product_catalog = Product_Catalog()

window = tk.Tk()

first_product = product_catalog.products_list[0]
first_product["amnt."] = 0
first_product["Total"] = 0

for i, key in enumerate(first_product):
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

        frm_value = tk.Frame(
            master=window,
            relief=tk.SUNKEN,
            height=4,
            borderwidth=1
        )
        frm_value.grid(row=i+1, column=j, padx=2, pady=2, sticky="nsew")

        lbl_value = tk.Label(
            master=frm_value,
            text=product[key],
            relief=tk.GROOVE,
            wraplength=400,
            height=3
        )
        lbl_value.pack(fill=tk.BOTH, expand=True, padx=1, pady=1)


window.mainloop()
