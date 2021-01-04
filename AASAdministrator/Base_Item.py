from textwrap import dedent
from Functions import format_price, add_iva, convert_to_pesos


class Item:

    def __init__(self, values):
        code, name, description, my_price, sell_price = values

        self.code = code
        self.name = name
        self.description = dedent(description)
        self.my_price = my_price
        self.my_price_iva = add_iva(my_price)
        self.sell_price = sell_price
        self.sell_price_iva = add_iva(sell_price)
