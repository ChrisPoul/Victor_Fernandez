import tkinter as tk
from Item import Item
from Product_Catalog import Product_Catalog

def get_product_values():
    product_values = [
        ent_group.get(),
        ent_line.get(),
        ent_code.get(),
        ent_name.get(),
        ent_description.get(),
        ent_brand.get(),
        ent_image.get(),
        float(ent_my_price.get()),
        float(ent_sell_price.get())
    ]

    product_catalog = Product_Catalog()
    product_catalog.add_product(product_values)
    print(product_catalog.product_names[-1])


window = tk.Tk()

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



lbl_code = tk.Label(
    master=frm_items,
    text="code"
)
lbl_code.grid(row=0, column=0, sticky="w")

ent_code = tk.Entry(
    master=frm_items,
    width=15
)
ent_code.grid(row=0, column=1, sticky="w")


lbl_name = tk.Label(
    master=frm_items,
    text="name"
)
lbl_name.grid(row=1, column=0, sticky="w")

ent_name = tk.Entry(
    master=frm_items,
    width=15
)
ent_name.grid(row=1, column=1, sticky="w")


lbl_description = tk.Label(
    master=frm_items,
    text="description"
)
lbl_description.grid(row=2, column=0, sticky="w")

ent_description = tk.Entry(
    master=frm_items,
    width=15
)
ent_description.grid(row=2, column=1, sticky="w")


lbl_brand = tk.Label(
    master=frm_items,
    text="brand"
)
lbl_brand.grid(row=3, column=0, sticky="w")

ent_brand = tk.Entry(
    master=frm_items,
    width=15
)
ent_brand.grid(row=3, column=1, sticky="w")


lbl_image = tk.Label(
master=frm_items,
text="image"
)
lbl_image.grid(row=4, column=0, sticky="w")

ent_image = tk.Entry(
master=frm_items,
width=15
)
ent_image.grid(row=4, column=1, sticky="w")


lbl_my_price = tk.Label(
    master=frm_items,
    text="my_price"
)
lbl_my_price.grid(row=5, column=0, sticky="w")

ent_my_price = tk.Entry(
    master=frm_items,
    width=15
)
ent_my_price.grid(row=5, column=1, sticky="w")


lbl_sell_price = tk.Label(
    master=frm_items,
    text="sell_price"
)
lbl_sell_price.grid(row=6, column=0, sticky="w")

ent_sell_price = tk.Entry(
    master=frm_items,
    width=15
)
ent_sell_price.grid(row=6, column=1, sticky="w")


btn_done = tk.Button(
    master=window,
    text="Done",
    command=get_product_values
)
btn_done.pack()

window.mainloop()
