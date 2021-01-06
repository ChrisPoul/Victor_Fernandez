from textwrap import dedent
from Functions import format_price, add_iva, convert_to_pesos


class Item:

    def __init__(self, values):
        group, line, code, name, description, brand, image, my_price, sell_price = values

        self.group = group
        self.line = line
        self.code = code
        self.name = name
        self.description = description
        self.brand = brand
        self.image = image

        self.my_price = float(my_price)
        self.my_price_iva = add_iva(self.my_price)
        self.sell_price = float(sell_price)
        self.sell_price_iva = add_iva(self.sell_price)
