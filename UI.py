from os import system
from Product_Catalog import Product_Catalog
from Functions import format_price, add_iva, convert_to_pesos

product_catalog = Product_Catalog()
products_list = product_catalog.products_list
names_list = product_catalog.products_list

stop_signal = 0
system("clear")
while stop_signal == 0:
    user_input = input('Type "exit" to exit\n')
    system("clear")

    if user_input == "exit":
        stop_signal = 1

    elif user_input.startswith("Sum"):
        my_total, sell_total = product_catalog.sum_mode()
        print(f"Mi total: {format_price(my_total)}")
        print(f"Mi total con IVA: {add_iva(my_total)}")
        print(f"Total de venta: {format_price(sell_total)}")
        print(f"Total de venta con IVA: {add_iva(sell_total)} USD o {add_iva(convert_to_pesos(sell_total))} MXN")

    elif user_input.startswith("Add Product"):
        user_inputs = []
        for key in product_catalog.products_list[0]:
            if key != "my_price_iva" and key != "sell_price_iva":
                user_inputs.append(input(f"{key}: "))

        product_catalog.add_product(user_inputs)

    for product in products_list:
        product_name = product["name"]

        if user_input in product:
            print(product[user_input])

        if product_name == product_catalog.get_correct_name(user_input):
            correct_product = product_catalog.get_correct_product(user_input)

            for attribute in correct_product:
                if attribute in user_input:
                    print(correct_product[attribute])

            if product_name == user_input:
                for attribute in correct_product:
                    print(f"{attribute} : {correct_product[attribute]}")
