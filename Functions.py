
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
    price_with_iva = round(price * 1.16, 2)

    return format_price(price_with_iva)


def convert_to_pesos(price):
    current_dollar_value = 19.88
    price_in_pesos = round(price * current_dollar_value, 2)

    return price_in_pesos


def get_repeated_characters(product_names):
    repeated_chars = product_names[0]
    for name in product_names:
        register = ""
        for i, char in enumerate(name):
            try:
                if char == repeated_chars[i]:
                    register += char

            except IndexError:
                pass

        repeated_chars = register

    return repeated_chars


def get_unique_characters(names):
    repeated_chars = get_repeated_characters(names)
    unique_chars = []

    for name in names:
        register = ""
        for i, char in enumerate(name):
            try:
                if char == repeated_chars[i]:
                    pass

            except IndexError:
                register += char

        unique_chars.append(register)

    return unique_chars
