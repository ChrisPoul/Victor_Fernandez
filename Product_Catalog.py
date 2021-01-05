from Item import Item
from Functions import get_name_list


def get_all_products(product_object_list):
    products = [vars(product) for product in product_object_list]

    return products


code = "SHELLY1"
name = "Shelly 1"
description = """
Relevador / Interruptor WIFI
Industrial y residencial inteligente /
Hasta 16A / Soporta Google /Alexa /
Nube P2P y control Local /"""
brand = "ALLTERCO ROBOTICS EOOD"
image = ""
my_price = 13.19
sell_price = 22.62
values = [code, name, description, brand, image, my_price, sell_price]
shelly_1 = Item(values)

code = "SHELLYPLUGS"
name = "Shelly Plug"
description = """
Adaptador WIFI NUBE P2P Shelly,
Tomacorriente, Calendarios,
MEDICIÓN DE CONSUMO"""
brand = "ALLTERCO ROBOTICS EOOD"
image = ""
my_price = 24.94
sell_price = 40.60
values = [code, name, description, brand, image, my_price, sell_price]
shelly_plug = Item(values)

code = "SHELLYDIMMER"
name = "Shelly Dimmer"
description = """
(MÁS PEQUEÑO DEL MUNDO) DIMMMER WIFI CLOUD /
Inalámbrico residencial inteligente
/ Protección de sobre carga / 16A
/ Soporta Google / Alexa / Nube P2P y local /"""
brand = "ALLTERCO ROBOTICS EOOD"
image = ""
my_price = 27.80
sell_price = 45.24
values = [code, name, description, brand, image, my_price, sell_price]
shelly_dimmer = Item(values)

code = "SHELLY25"
name = "Shelly 25"
description = """
Doble Relevador / Interruptor WIFI
CLOUD Industrial y residencial
Inteligente / Medidor de consumo /
10A / Soporta Google /Alexa /
Nube P2P y local / Ideal para
persinas y garage"""
brand = "ALLTERCO ROBOTICS EOOD"
image = ""
my_price = 21.38
sell_price = 45.24
values = [code, name, description, brand, image, my_price, sell_price]
shelly_25 = Item(values)

code = "SHELLY1PM"
name = "Shelly 1 PM"
description = """
Relevador / Interruptor WIFI CLOUD
/ Industrial y residencial Inteligente
/ Medidor de consumo, protección
hasta 3500W / 16A / Soporta
Google / Alexa / Nube P2P y
control local /"""
brand = "ALLTERCO ROBOTICS EOOD"
image = ""
my_price = 16.39
sell_price = 33.64
values = [code, name, description, brand, image, my_price, sell_price]
shelly_1_pm = Item(values)

code = "SHELLYHT"
name = "Shelly HT"
description = """
Sensor inalámbrico de temperatura
y humedad, App gratis, métricas de
lectura en graficas y notificaciones
en celular."""
brand = "ALLTERCO ROBOTICS EOOD"
image = ""
my_price = 26.37
sell_price = 42.92
values = [code, name, description, brand, image, my_price, sell_price]
shelly_ht = Item(values)

code = "SHELLY-RGBW2"
name = "Shelly RGBW2"
description = """
Relevador inalámbrico para el
control de iluminación color en
tiras LED."""
brand = "ALLTERCO ROBOTICS EOOD"
image = ""
my_price = 28.51
sell_price = 46.40
values = [code, name, description, brand, image, my_price, sell_price]
shelly_rgbw2 = Item(values)

code = "SHELLY1L"
name = "Shelly 1L"
description = """
Relevador SIN usar cable Neutro /
Interruptor WIFI INDUSTRIAL
Industrial y residencial inteligente /
Hasta 5A / Soporta Google /Alexa /
Nube P2P y control Local /"""
brand = "ALLTERCO ROBOTICS EOOD"
image = ""
my_price = 21.38
sell_price = 34.80
values = [code, name, description, brand, image, my_price, sell_price]
shelly_1l = Item(values)

code = "HC7"
name = "Shelly HC7"
description = """
HUB Controlador inteligente para
dispositivos Zwave, Zigbee,
integrable con Shelly, Lutron entre
otras, APP gratis sin pago de
anualidad o mensualidad."""
brand = "ALLTERCO ROBOTICS EOOD"
image = ""
my_price = 144.68
sell_price = 235.48
values = [code, name, description, brand, image, my_price, sell_price]
shelly_hc7 = Item(values)

product_list = [
    shelly_1, shelly_1l, shelly_hc7,
    shelly_plug, shelly_dimmer, shelly_25,
    shelly_1_pm, shelly_ht, shelly_rgbw2
]


class Product_Catalog:

    def __init__(self):
        self.product_catalog = get_all_products(product_list)
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


    def get_product(self, name):
        dictionary_list = self.product_catalog
        for dictionary in dictionary_list:
            if dictionary["name"] == name:
                return dictionary


    def get_correct_product(self, search_term):
        dictionary_list = self.product_catalog
        name_list = get_name_list(dictionary_list)
        correct_name = self.get_correct_name(search_term)

        return self.get_product(correct_name)


    def sum_products(self, name_and_cuantity):
        total = 0
        for product_name in name_and_cuantity:
            product_cuantity = name_and_cuantity[product_name]

            product_attributes = self.get_product(product_name)
            unit_price = product_attributes["my_price"]

            product_total_price = unit_price * product_cuantity
            total += product_total_price

        return round(total, 2)


    def add_product(self, values):
        new_product = Item(values)
        new_product_dict = vars(new_product)
        new_product_name = new_product_dict["name"]

        self.product_catalog.append(new_product_dict)
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
