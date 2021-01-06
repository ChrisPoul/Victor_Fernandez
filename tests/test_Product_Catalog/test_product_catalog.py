from Product_Catalog import Product_Catalog


product_catalog = Product_Catalog()


def test_get_correct_name():
    assert product_catalog.get_correct_name("Shelly 1 PM bla bla") == "Shelly 1 PM"
    assert product_catalog.get_correct_name("some random thing") == ""
    assert product_catalog.get_correct_name("") == ""


def test_get_product():
    assert product_catalog.get_product("Shelly 1L") == product_catalog.products_list[1]
    assert product_catalog.get_product("Shelly 1") == product_catalog.products_list[0]


def test_get_correct_product():
    assert product_catalog.get_correct_product("Shelly 1 PM op") == product_catalog.products_list[-3]
    assert product_catalog.get_correct_product("Shelly 1 23d 21d") == product_catalog.products_list[0]
