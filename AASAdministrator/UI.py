from os import system
from Shelly import Shelly_1, Shelly_1L, Shelly_HC7, Shelly_Plug, Shelly_RGBW2
from Shelly import Shelly_Dimmer, Shelly_25, Shelly_1_PM, Shelly_HT

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
stop_signal = 0
system("clear")

while stop_signal == 0:
    user_input = input('Type "exit" to exit\n')

    system("clear")

    if user_input == "exit":
        stop_signal = 1

    for shelly in shellies:
        my_dict = vars(shelly)
        if user_input in my_dict:
            print(my_dict[user_input])

        elif my_dict["name"] + " " in user_input:
            numbers = "1234567890"
            user_input = user_input[user_input.find("Add"):]
            if "Add" in user_input:
                to_add = ""
                for char in user_input:
                    if char in numbers:
                        to_add += char
            total = my_dict["customer_price"] * int(to_add)
            print(to_add)
            print(f"total {total}")

            print(my_dict["code"])
