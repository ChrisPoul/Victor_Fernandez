from Product_Catalog import get_all_products, Product_Catalog


product_catalog = Product_Catalog()


def test_get_attribute_values():
    search_term = "Bla bla name"

    assert product_catalog.get_attribute_values(search_term) == product_catalog.product_names


def test_get_correct_name():
    assert product_catalog.get_correct_name("Shelly 1 PM bla bla") == "Shelly 1 PM"
    assert product_catalog.get_correct_name("some random thing") == ""
    assert product_catalog.get_correct_name("") == ""


def test_get_product():
    assert product_catalog.get_product("Shelly 1L") == product_catalog.product_catalog[1]
    assert product_catalog.get_product("Shelly 1") == product_catalog.product_catalog[0]


def test_get_correct_product():
    assert product_catalog.get_correct_product("Shelly 1 PM op") == product_catalog.product_catalog[-3]
    assert product_catalog.get_correct_product("Shelly 1 23d 21d") == product_catalog.product_catalog[0]


def test_add_product():
    test_values = [
    "TEST", "Test", "A test object", "Test Brand", "an image", "10.5", "20.72"
    ]
    product_catalog.add_product(test_values)

    assert product_catalog.product_catalog[-1]["name"] == "Test"
    assert product_catalog.product_catalog[-1]["my_price"] == 10.5
    assert product_catalog.product_catalog[-1]["sell_price"] == 20.72
    assert product_catalog.product_names[-1] == "Test"


def test_sum_products():
    product_name_cuantity1 = {"Shelly 1": 1, "Shelly 1 PM": 1}
    product_name_cuantity2 = {"Shelly 1": -1, "Shelly 1 PM": 1}
    product_name_cuantity3 = {"Shelly 1": 1, "Shelly 1 PM": -1}


    assert product_catalog.sum_products(product_name_cuantity1) == 29.58
    assert product_catalog.sum_products(product_name_cuantity2) == 3.2
    assert product_catalog.sum_products(product_name_cuantity3) == -3.2
