from Shelly import Shelly_1, Shelly_1L, Shelly_HC7, Shelly_Plug, Shelly_RGBW2
from Shelly import Shelly_Dimmer, Shelly_25, Shelly_1_PM, Shelly_HT
from Functions import get_name_list, get_correct_object, get_correct_name


def get_all_products(product_list):
    products = []
    for product_sub_list in product_list:
        products += [vars(product) for product in product_sub_list]

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
        self.product_names = get_name_list(self.product_catalog)


    def get_product_attributes(self, product_name):
        for product in self.product_catalog:
            if product_attributes["name"] == product_name:
                return product_attributes


    def add_products(self, products):
        total = 0
        for product_name in products:
            product_cuantity = products[product_name]

            product_attributes = self.get_product_attributes(product_name)
            unit_price = product_attributes["my_price"]

            product_total_price = unit_price * product_cuantity
            total += product_total_price

        return total


    def sum_mode(self):
        stop_signal = 0
        my_total = 0
        sell_total = 0
        while stop_signal == 0:
            user_input = input("Enter product and cuantity:\n")

            if user_input == "exit" or user_input == "":
                stop_signal = 1
                break

            product_name = get_correct_name(user_input, self.product_names)

            if product_name == "" or product_name not in self.product_names:
                print("Not an option")

            else:
                product = get_correct_object(user_input, self.product_catalog)
                unit_my_price = product["my_price"]
                unit_sell_price = product["sell_price"]

                start = len(product_name) + 1
                cuantity = user_input[start:].strip(" ")
                try:
                    cuantity = int(cuantity)
                    my_total += unit_my_price * cuantity
                    sell_total += unit_sell_price * cuantity

                except ValueError:
                    print("Not a valid number, try again.")

        return my_total, sell_total
