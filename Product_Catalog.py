from Item import Item
from Functions import get_name_list, get_product_total
import json


def open_database():
    with open("Product_Database.json", "r") as database:
        product_list = json.load(database)

        return product_list


def close_database(product_list):
    json_data = json.dumps(product_list, indent=4)

    with open("Product_Database.json", "w") as database:
        database.write(json_data)


class Product_Catalog:

    def __init__(self):
        self.products_list = open_database()
        self.product_names = get_name_list(self.products_list)


    def get_initial_keys(self):
        pass


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


    def get_product(self, name):
        dictionary_list = self.products_list
        for dictionary in dictionary_list:
            if dictionary["name"] == name:
                return dictionary


    def get_correct_product(self, search_term):
        dictionary_list = self.products_list
        name_list = get_name_list(dictionary_list)
        correct_name = self.get_correct_name(search_term)

        return self.get_product(correct_name)


    def add_product(self, values):
        new_product = Item(values)
        new_product_dict = vars(new_product)
        new_product_name = new_product_dict["name"]

        self.products_list.append(new_product_dict)
        close_database(self.products_list)
        self.product_names.append(new_product_name)


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
                product = self.get_product(product_name)
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
