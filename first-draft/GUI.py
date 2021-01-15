import tkinter as tk
from Product_Catalog import Product_Catalog
from Receipt_GUI import Receipt_GUI
from Inventory_GUI import Inventory_GUI
from Product_Manager_GUI import Product_Manager_GUI


window = tk.Tk()

def open_receipt():
    frame.destroy()
    frm_receipt = tk.Frame(
        master=window
    )
    frm_receipt.pack(fill=tk.BOTH, expand=True)

    receipt = Receipt_GUI(frm_receipt)


def open_inventory():
    frame.destroy()

    frm_inventory = tk.Frame(
        master=window
    )
    frm_inventory.pack(fill=tk.BOTH, expand=True)

    inventory = Inventory_GUI(frm_inventory)


def open_product_manager():
    frame.destroy()

    frm_product_manager = tk.Frame(
        master=window
    )
    frm_product_manager.pack(fill=tk.BOTH, expand=True)
    product_manager = Product_Manager_GUI(frm_product_manager)


frame = tk.Frame(
    master=window
)
frame.pack(fill=tk.BOTH, expand=True)

btn_receipt = tk.Button(
    master=frame,
    text="Receipt",
    command=open_receipt
)
btn_receipt.pack()

btn_inventory = tk.Button(
    master=frame,
    text="Inventory",
    command=open_inventory
)
btn_inventory.pack()

btn_product_manager = tk.Button(
    master=frame,
    text="Product Manager",
    command=open_product_manager
)
btn_product_manager.pack()


window.mainloop()
