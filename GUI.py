import tkinter as tk
from Product_Catalog import Product_Catalog

product_catalog = Product_Catalog()

window = tk.Tk()
window.rowconfigure([0, 1], weight=1, minsize=1)

product = product_catalog.product_catalog[0]
for i, key in enumerate(product):
    window.columnconfigure(i, weight=1, minsize=50)

    frame = tk.Frame(
        master=window,
        relief=tk.RAISED,
        borderwidth=1
    )
    frame.grid(row=0, column=i, padx=3, pady=3, sticky="ew")

    lbl_key = tk.Label(
        master=frame,
        text=key,
        relief=tk.RIDGE,
        height=2,
        borderwidth=1
    )
    lbl_key.pack(fill=tk.X, padx=5, pady=5)

    lbl_value = tk.Label(
        master=frame,
        text=product[key],
        relief=tk.SUNKEN,
        height=6
    )
    lbl_value.pack(fill=tk.X, padx=5, pady=5)


window.columnconfigure(i+1, weight=1, minsize=50)
frm_amnt = tk.Frame(
    master=window,
    relief=tk.RAISED,
    borderwidth=1
)
frm_amnt.grid(row=0, column=i+1, padx=3, pady=3, sticky="w")

lbl_amnt = tk.Label(
    master=frm_amnt,
    text="amnt.",
    relief=tk.RIDGE,
    height=2,
    width=5,
    borderwidth=1
)
lbl_amnt.pack(padx=5, pady=5)

lbl_amnt_value = tk.Label(
    master=frm_amnt,
    text=0,
    relief=tk.SUNKEN,
    height=6,
    width=5,
    borderwidth=1
)
lbl_amnt_value.pack(padx=5, pady=5)


window.mainloop()
