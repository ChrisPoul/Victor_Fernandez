from AASAdministrator.Product_Catalog import get_all_products, Product_Catalog


product_catalog = Product_Catalog()


def test_get_attribute_values():
    search_term = "Bla bla name"

    assert product_catalog.get_attribute_values(search_term) == product_catalog.product_names
    

def test_get_correct_name():
    assert product_catalog.get_correct_name("Shelly 1 PM bla bla") == "Shelly 1 PM"
    assert product_catalog.get_correct_name("some random thing") == ""
    assert product_catalog.get_correct_name("") == ""


def test_get_object():
    assert product_catalog.get_object("Shelly 1L") == product_catalog.product_catalog[1]
    assert product_catalog.get_object("Shelly 1") == product_catalog.product_catalog[0]


def test_get_correct_object():
    assert product_catalog.get_correct_object("Shelly 1 PM op") == product_catalog.product_catalog[-3]
    assert product_catalog.get_correct_object("Shelly 1 23d 21d") == product_catalog.product_catalog[0]


def test_add_products():
    product_name_cuantity1 = {"Shelly 1": 1, "Shelly 1 PM": 1}
    product_name_cuantity2 = {"Shelly 1": -1, "Shelly 1 PM": 1}
    product_name_cuantity3 = {"Shelly 1": 1, "Shelly 1 PM": -1}


    assert product_catalog.add_products(product_name_cuantity1) == 29.58
    assert product_catalog.add_products(product_name_cuantity2) == 3.2
    assert product_catalog.add_products(product_name_cuantity3) == -3.2
