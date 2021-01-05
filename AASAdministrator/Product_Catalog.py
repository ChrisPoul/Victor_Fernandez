from AASAdministrator.Shelly import Shelly_1, Shelly_1L, Shelly_HC7, Shelly_Plug, Shelly_RGBW2
from AASAdministrator.Shelly import Shelly_Dimmer, Shelly_25, Shelly_1_PM, Shelly_HT
from AASAdministrator.Functions import get_name_list


def get_all_products(product_object_list):
    products = []
    for product_sub_list in product_object_list:
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


    def get_attribute_values(self, search_term):
        values = []
        dict_list = self.product_catalog

        for dictionary in dict_list:
            for attribute in dictionary:
                if attribute in search_term:
                    values.append(dictionary[attribute])

        return values


    def get_correct_name(self, search_term):
        names_list = self.product_names
        similar_names = [name for name in names_list if name in search_term]

        max_len = 0
        larger_name = ""
        for name in similar_names:
            if len(name) > max_len:
                max_len = len(name)
                larger_name = name

        return larger_name


    def get_object(self, name):
        dictionary_list = self.product_catalog
        for dictionary in dictionary_list:
            if dictionary["name"] == name:
                return dictionary


    def get_correct_object(self, search_term):
        dictionary_list = self.product_catalog
        name_list = get_name_list(dictionary_list)
        correct_name = self.get_correct_name(search_term)

        return self.get_object(correct_name)


    def add_products(self, name_and_cuantity):
        total = 0
        for product_name in name_and_cuantity:
            product_cuantity = name_and_cuantity[product_name]

            product_attributes = self.get_object(product_name)
            unit_price = product_attributes["my_price"]

            product_total_price = unit_price * product_cuantity
            total += product_total_price

        return round(total, 2)


    def sum_mode(self):
        stop_signal = 0
        my_total = 0
        sell_total = 0
        while stop_signal == 0:
            user_input = input("Enter product and cuantity:\n")

            if user_input == "exit" or user_input == "":
                stop_signal = 1
                break

            product_name = self.get_correct_name(user_input)

            if product_name == "" or product_name not in self.product_names:
                print("Not an option")

            else:
                product = self.get_object(product_name)
                my_unit_price = product["my_price"]
                unit_sell_price = product["sell_price"]

                start = len(product_name) + 1
                cuantity = user_input[start:].strip(" ")
                try:
                    cuantity = int(cuantity)
                    my_total += my_unit_price * cuantity
                    sell_total += unit_sell_price * cuantity

                except ValueError:
                    print("Not a valid number, try again.")

        return my_total, sell_total
