import tkinter as tk

def get_name_list(dictionary_list):
    names = [dictionary["name"] for dictionary in dictionary_list]

    return names


def add_commas_price(price):
    price_parts = price.split(".")
    price_int = price_parts[0]

    comma_track = 1
    int_with_commas = ""
    for i, num in enumerate(price_int[::-1]):
        int_with_commas += num
        if comma_track == 3 and i != len(price_int)-1:
            int_with_commas += ","
            comma_track = 0

        comma_track += 1

    price_with_commas = f"{int_with_commas[::-1]}.{price_parts[1]}"

    return price_with_commas


def format_price(price):
    price = str(price)
    if "." not in price:
        price += ".00"

    elif price[-2] == ".":
        price += "0"

    price_with_commas = add_commas_price(price)

    return f"${price_with_commas}"


def add_iva(price):
    try:
        price_with_iva = round(price * 1.16, 2)

    except TypeError:
        price_with_iva = 0

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

    return round(grand_total, 2)


def top_row(frm_body, wanted_names):
    for i, key in enumerate(wanted_names):
        frm_body.rowconfigure(0, weight=1)
        frm_body.columnconfigure(i, weight=1)

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


def main_body(frm_body, products, wanted_names):

    top_row(frm_body, wanted_names)

    def get_total():
        user_input = ent_amnt.get()
        amnt = int(user_input)
        total = get_product_total(product, amnt)
        lbl_value["text"] = add_iva(total)


    for i, product in enumerate(products):
        frm_body.rowconfigure(i+1, weight=1)

        for j, key in enumerate(wanted_names):
            frm_body.columnconfigure(j, weight=1)
            value = product[key]
            my_wrap_length = 400
            my_justify = "left"

            if key == "my_price" or key == "sell_price":
                value = format_price(value)

            elif key == "brand":
                my_wrap_length = 60
                my_justify = "center"

            frm_value = tk.Frame(
                master=frm_body,
                relief=tk.SUNKEN,
                borderwidth=1
            )
            frm_value.grid(row=i+1, column=j, padx=2, pady=2, sticky="nsew")

            lbl_value = tk.Label(
                master=frm_value,
                text=value,
                relief=tk.GROOVE,
                wraplength=my_wrap_length,
                justify=my_justify
            )
            lbl_value.pack(fill=tk.BOTH, expand=True, padx=1, pady=1)
