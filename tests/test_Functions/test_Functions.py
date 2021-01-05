from AASAdministrator.Functions import format_price, add_iva, convert_to_pesos, get_name_list
from AASAdministrator.Functions import get_repeated_characters, get_unique_characters


def test_get_name_list():
    dictionary_list = [{"name":"Shelly 1", "code": "SHELLY1"}, {"name":"Shelly 1 PM", "code": "SHELLY1PM"}]
    empty_list = []

    assert get_name_list(dictionary_list) == ["Shelly 1", "Shelly 1 PM"]
    assert get_name_list(empty_list) == []


def test_format_price():
    assert format_price(10.0) == "$10.00"
    assert format_price(58.49) == "$58.49"
    assert format_price(1) == "$1.00"
    assert format_price(-1) == "$-1.00"
    assert format_price(0) == "$0.00"


def test_add_iva():
    price1 = 100.0
    price2 = 832.13

    assert add_iva(price1) == "$116.00"
    assert add_iva(price2) == "$965.27"


def test_convert_to_pesos():
    dollars1 = 1.0
    dollars2 = 48.0

    assert convert_to_pesos(dollars1) == 19.88
    assert convert_to_pesos(dollars2) == 954.24


def test_get_repeated_characters():
    names_list = ["Shelly 1", "Shelly 1 PM", "Shelly Plug"]

    assert get_repeated_characters(names_list) == "Shelly "


def test_get_unique_characters():
    names_list = ["Shelly 1", "Shelly 1 PM", "Shelly Plug"]

    assert get_unique_characters(names_list) == ["1", "1 PM", "Plug"]
