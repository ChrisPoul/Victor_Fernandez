
def some_filter(thing):
    pass


def format_price(price):
    price = str(price)
    if price[-2:] == ".0":
        price += "0"

    return f"${price}"


def add_iva(price):
    price_with_iva = round(price * 1.16, 2)

    return format_price(price_with_iva)


def convert_to_pesos(price):
    current_dollar_value = 19.88
    price_in_pesos = round(price * current_dollar_value, 2)

    return format_price(price_in_pesos)
