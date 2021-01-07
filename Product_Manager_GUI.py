import tkinter as tk
from Item import Item
from Product_Catalog import Product_Catalog
from Item import Product


class Product_Manager_GUI(Product_Catalog):

    def __init__(self, window):
        product = Product()
        product = vars(product)
        Product_Catalog.__init__(self)
        self.window = window

        keys = [key for key in product]
        self.first_two = keys[:2]
        self.fields = keys[2:]
        self.entries = []

        self.main_body()


    def top_part(self):
        for key in self.first_two:
            frm = tk.Frame(
                master=self.window
            )
            frm.pack()

            lbl = tk.Label(
                master=frm,
                text=f"{key}:"
            )
            lbl.pack()
            ent = tk.Entry(
                master=frm
            )
            ent.pack()

            frm_empty = tk.Frame(
                master=self.window,
                height=50
            )
            frm_empty.pack()

            self.entries.append(ent)


    def main_body(self):
        window = self.window

        self.top_part()

        frm_product = tk.Frame(
            master=window
        )
        frm_product.pack()

        lbl_product = tk.Label(
            master=frm_product,
            text="Enter Product:"
        )
        lbl_product.pack()

        frm_items = tk.Frame(
            master=frm_product
        )
        frm_items.pack(side=tk.LEFT)

        for i, field in enumerate(self.fields):
            lbl_attribute = tk.Label(
                master=frm_items,
                text=field
            )
            lbl_attribute.grid(row=i, column=0)

            ent_attribute = tk.Entry(
                master=frm_items
            )
            ent_attribute.grid(row=i, column=1)
            self.entries.append(ent_attribute)

        def get_user_input():
            values = []
            for entry in self.entries:
                values.append(entry.get())
                entry.delete(0, tk.END)

            self.add_product(values)


        btn_done = tk.Button(
            master=window,
            text="Done",
            command=get_user_input
        )
        btn_done.pack()
