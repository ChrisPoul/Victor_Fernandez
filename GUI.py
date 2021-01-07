import tkinter as tk
from Product_Catalog import Product_Catalog
from Receipt import Receipt
from Functions import format_price, add_iva, get_product_total

product_catalog = Product_Catalog()
receipt = Receipt()
window = tk.Tk()

for key in receipt.wanted_names:
    receipt.first_row(window)

receipt.body(window, product_catalog.products_list)

window.mainloop()
