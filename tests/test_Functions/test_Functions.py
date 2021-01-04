from AASAdministrator.Functions import format_price, add_iva, convert_to_pesos
from AASAdministrator.Functions import some_filter


def test_format_price():
    price1 = 10.0
    price2 = 58.49
    price3 = 7291.5

    assert format_price(price1) == "$10.00"
    assert format_price(price2) == "$58.49"
    assert format_price(price3) == "$7291.5"


def test_add_iva():
    price1 = 100.0
    price2 = 832.13

    assert add_iva(price1) == "$116.00"
    assert add_iva(price2) == "$965.27"


def test_convert_to_pesos():
    dollars1 = 1.0
    dollars2 = 48.0

    assert convert_to_pesos(dollars1) == "$19.88"
    assert convert_to_pesos(dollars2) == "$954.24"


def test_some_filter():
    user_input = "Shelly 1 PM"

    assert some_filter(user_input) == "Shelly 1 PM"
