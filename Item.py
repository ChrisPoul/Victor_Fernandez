from textwrap import dedent
from Functions import format_price, add_iva, convert_to_pesos


class Item:

    def __init__(self, values):
        code, name, description, brand, image, my_price, sell_price = values

        self.code = code
        self.name = name
        self.description = dedent(description)
        self.brand = brand
        self.image = image

        self.my_price = float(my_price)
        self.sell_price = float(sell_price)


    def prices_iva(self):
        my_price_iva = add_iva(self.my_price)
        sell_price_iva = add_iva(self.sell_price)

        return my_price_iva, sell_price_iva
