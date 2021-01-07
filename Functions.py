import tkinter as tk

def get_name_list(dictionary_list):
    names = [dictionary["name"] for dictionary in dictionary_list]

    return names


def format_price(price):
    price = str(price)
    if "." not in price:
        price += ".00"

    elif price[-2] == ".":
        price += "0"

    return f"${price}"


def add_iva(price):
    try:
        price_with_iva = round(price * 1.16, 2)

    except TypeError:
        return "error"

    return format_price(price_with_iva)


def convert_to_pesos(price):
    current_dollar_value = 19.88
    price_in_pesos = round(price * current_dollar_value, 2)

    return price_in_pesos


def get_product_total(product, cuantity):
    total = 0
    unit_price = float(product["sell_price"])

    total = unit_price * int(cuantity)

    return round(total, 2)


def add_totals(totals_lst):
    grand_total = 0
    for total in totals_lst:
        grand_total += float(total)

    return grand_total


def first_row(frm_body, wanted_names):
    for i, key in enumerate(wanted_names):
        frm_body.rowconfigure(0, weight=1, minsize=50)
        frm_body.columnconfigure(i, weight=1, minsize=50)

        key_frame = tk.Frame(
            master=frm_body,
            relief=tk.RAISED,
            borderwidth=1
        )
        key_frame.grid(row=0, column=i, padx=2, pady=5, sticky="ews")

        key_lbl = tk.Label(
            master=key_frame,
            text=wanted_names[key],
            height=2
        )
        key_lbl.pack(fill=tk.X, expand=True, side=tk.BOTTOM)
