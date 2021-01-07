import tkinter as tk
from Product_Catalog import Product_Catalog
from Receipt import Receipt
from Functions import format_price, add_iva, get_product_total

product_catalog = Product_Catalog()
products = product_catalog.products_list

receipt = Receipt()

window = tk.Tk()

frm_body = tk.Frame(
    master=window
)
frm_body.pack(fill=tk.BOTH, expand=True)

frm_main_body = tk.Frame(
    master=frm_body
)
frm_main_body.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)
receipt.main_body(frm_main_body, products)

frm_totals_body = tk.Frame(
    master=frm_body
)
frm_totals_body.pack(fill=tk.BOTH, expand=True, side=tk.RIGHT)
receipt.totals_body(frm_totals_body, products)

frm_submit = tk.Frame(
    master=window,
    height=2
)
frm_submit.pack(fill=tk.X)
receipt.submit(frm_submit, products)


window.mainloop()
