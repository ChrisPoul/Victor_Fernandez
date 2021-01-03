from textwrap import dedent


def format_price(price):
    if price[-2:] == ".0":
        price += "0"

        return f"${price}"



def add_iva(price):
    price_with_iva = str(round(price * 1.16, 2))

    return format_price(price_with_iva)



def convert_to_pesos(price):
    current_dollar_value = 19.88
    price_in_pesos = str(round(price * current_dollar_value))

    return format_price(price_in_pesos)


def get_total(items):
    pass


class Item:

    def __init__(self, values):
        code, name, description, my_price, sell_price = values

        self.code = code
        self.name = name
        self.description = dedent(description)
        self.wholesaler_price = my_price
        self.wholesaler_price_iva = add_iva(my_price)
        self.customer_price = sell_price
        self.customer_price_iva = add_iva(sell_price)
