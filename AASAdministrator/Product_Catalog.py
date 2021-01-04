from Shelly import Shelly_1, Shelly_1L, Shelly_HC7, Shelly_Plug, Shelly_RGBW2
from Shelly import Shelly_Dimmer, Shelly_25, Shelly_1_PM, Shelly_HT


def get_all_products(product_list):
    products = []
    for product_sub_list in product_list:
        products += [product for product in product_sub_list]

    return products


shelly_1 = Shelly_1()
shelly_plug = Shelly_Plug()
shelly_dimmer = Shelly_Dimmer()
shelly_25 = Shelly_25()
shelly_1_pm = Shelly_1_PM()
shelly_ht = Shelly_HT()
shelly_rgbw2 = Shelly_RGBW2()
shelly_1l = Shelly_1L()
shelly_hc7 = Shelly_HC7()

shellies = [
    shelly_1, shelly_1l, shelly_hc7,
    shelly_plug, shelly_dimmer, shelly_25,
    shelly_1_pm, shelly_ht, shelly_rgbw2
]

product_main_list = [shellies]

class Product_Catalog:

    def __init__(self):
        self.product_catalog = get_all_products(product_main_list)


    def get_product_attributes(self, product_name):
        for product in self.product_catalog:
            product_attributes = vars(product)
            if product_attributes["name"] == product_name:
                return product_attributes


    def add_products(self, user_input):
        products_with_cuantity = user_input.split("+")
        total = 0
        for product_with_cuantity in products_with_cuantity:
            start = product_with_cuantity.find(" ", 1) + 1
            space_index = product_with_cuantity.find(" ", start)

            if product_with_cuantity.startswith(" "):
                product_name = product_with_cuantity[1:space_index]

            else:
                product_name = product_with_cuantity[:space_index]

            cuantity_with_space = product_with_cuantity[space_index:]
            cuantity = int(cuantity_with_space.strip(" "))

            product_attributes = self.get_product_attributes(product_name)
            unit_price = product_attributes["wholesaler_price"]

            product_total = unit_price * cuantity
            total += product_total

        return total
