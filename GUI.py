import tkinter as tk
from Product_Catalog import Product_Catalog
from Receipt import Receipt
from Functions import format_price, add_iva, get_product_total

product_catalog = Product_Catalog()
receipt = Receipt()
window = tk.Tk()

frm_body = tk.Frame(
    master=window
)
frm_body.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)

frm_main_body = tk.Frame(
    master=frm_body
)
frm_main_body.pack(fill=tk.BOTH, expand=True)

receipt.first_row(frm_main_body)

receipt.main_body(frm_main_body, product_catalog.products_list)

frm_totals_body = tk.Frame(
    master=frm_body
)
frm_totals_body.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)

receipt.totals_body(frm_totals_body)

frm_submit = tk.Frame(
    master=window,
    height=2
)
frm_submit.pack(fill=tk.X)

window.mainloop()
