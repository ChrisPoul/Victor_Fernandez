import tkinter as tk
from Product_Catalog import Product_Catalog

product_catalog = Product_Catalog()

window = tk.Tk()

top_frm = tk.Frame(
    master=window,
    relief=tk.GROOVE,
    borderwidth=2
)
top_frm.pack(fill=tk.X, expand=True,)

for key in product_catalog.products_list[0]:
    key_frame = tk.Frame(
        master=top_frm,
        relief=tk.RIDGE,
        borderwidth=1
    )
    key_frame.pack(fill=tk.X, expand=True, side=tk.LEFT)

    key_lbl = tk.Label(
        master=key_frame,
        text=key,
        height=1
    )
    key_lbl.pack(fill=tk.X, expand=True, padx=5, pady=5)

bottom_frm = tk.Frame(
    master=window,
    borderwidth=1
)
bottom_frm.pack(fill=tk.BOTH, expand=True)

for i, product in enumerate(product_catalog.products_list):
    product["amnt."] = 0
    product["Total"] = 0

    bottom_frm.rowconfigure(i, weight=1, minsize=50)

    for j, key in enumerate(product):
        bottom_frm.columnconfigure(j, weight=1, minsize=50)

        main_frame = tk.Frame(
            master=bottom_frm,
            relief=tk.RAISED,
            borderwidth=1
        )
        main_frame.grid(row=i, column=j, padx=2, pady=2, sticky="nsew")

        frm_value = tk.Frame(
            master=main_frame,
            relief=tk.SUNKEN,
            borderwidth=1
        )
        frm_value.pack(fill=tk.X, expand=True)

        lbl_value = tk.Label(
            master=frm_value,
            text=product[key],
            height=5
        )
        lbl_value.pack(fill=tk.X, expand=True)


window.mainloop()
