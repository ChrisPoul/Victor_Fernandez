import tkinter as tk
from Item import Item
from Product_Catalog import Product_Catalog


class Product_Manager_GUI(Product_Catalog):

    def __init__(self, window):
        Product_Catalog.__init__(self)
        self.window = window
        self.fields = [attribute for attribute in self.products_list[0] if "iva" not in attribute][2:]

        self.main_body()


    def main_body(self):
        window = self.window

        frm_group = tk.Frame(
            master=window
        )
        frm_group.pack()

        lbl_group = tk.Label(
            master=frm_group,
            text="Enter a Group:"
        )
        lbl_group.pack()
        ent_group = tk.Entry(
            master=frm_group
        )
        ent_group.pack()

        frm_empty = tk.Frame(
            master=window,
            height=50
        )
        frm_empty.pack()


        frm_line = tk.Frame(
            master=window
        )
        frm_line.pack()


        lbl_line = tk.Label(
            master=frm_line,
            text="Enter a Line:"
        )
        lbl_line.pack()
        ent_line = tk.Entry(
            master=frm_line
        )
        ent_line.pack()


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

        entries = [ent_group, ent_line]
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
            entries.append(ent_attribute)

        def get_user_input():
            values = []
            for entry in entries:
                values.append(entry.get())
                entry.delete(0, tk.END)

            product_catalog.add_product(values)


        btn_done = tk.Button(
            master=window,
            text="Done",
            command=get_user_input
        )
        btn_done.pack()
