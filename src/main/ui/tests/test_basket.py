from faker import Faker

from src.main.ui.steps.basket_steps import BasketSteps
from src.main.ui.steps.catalog_steps import CatalogSteps
from src.main.ui.steps.checkout_steps import CheckoutSteps

fake = Faker()


def test_add_item_and_check_in_cart(page):
    catalog = CatalogSteps(page)
    basket = BasketSteps(page)

    catalog.login("standard_user", "secret_sauce")
    catalog.add_to_cart("Sauce Labs Backpack")

    basket.open_cart()
    basket.expect_item_in_cart("Sauce Labs Backpack")


def test_add_items_and_check_in_cart(page):
    catalog = CatalogSteps(page)
    basket = BasketSteps(page)

    catalog.login("standard_user", "secret_sauce")
    catalog.add_to_cart("Sauce Labs Fleece Jacket")
    catalog.add_to_cart("Sauce Labs Bolt T-Shirt")

    basket.open_cart()
    basket.expect_item_in_cart("Sauce Labs Fleece Jacket")
    basket.expect_item_in_cart("Sauce Labs Bolt T-Shirt")


def test_remove_item_from_cart(page):
    catalog = CatalogSteps(page)
    basket = BasketSteps(page)

    catalog.login("standard_user", "secret_sauce")
    catalog.add_to_cart("Sauce Labs Fleece Jacket")

    basket.open_cart()
    basket.expect_item_in_cart("Sauce Labs Fleece Jacket")

    basket.remove_from_cart("Sauce Labs Fleece Jacket")
    basket.expect_item_not_in_cart("Sauce Labs Fleece Jacket")


def test_remove_items_from_cart(page):
    catalog = CatalogSteps(page)
    basket = BasketSteps(page)

    catalog.login("standard_user", "secret_sauce")
    catalog.add_to_cart("Sauce Labs Backpack")
    catalog.add_to_cart("Test.allTheThings() T-Shirt (Red)")

    basket.open_cart()
    basket.expect_item_in_cart("Sauce Labs Backpack")
    basket.expect_item_in_cart("Test.allTheThings() T-Shirt (Red)")

    basket.remove_from_cart("Sauce Labs Backpack")
    basket.remove_from_cart("Test.allTheThings() T-Shirt (Red)")

    basket.expect_item_not_in_cart("Sauce Labs Backpack")
    basket.expect_item_not_in_cart("Test.allTheThings() T-Shirt (Red)")


def test_checkout_multiple_items(page):
    catalog = CatalogSteps(page)
    basket = BasketSteps(page)
    checkout = CheckoutSteps(page)

    catalog.login("standard_user", "secret_sauce")
    catalog.add_to_cart("Sauce Labs Fleece Jacket")
    catalog.add_to_cart("Sauce Labs Bolt T-Shirt")

    basket.open_cart()
    basket.expect_item_in_cart("Sauce Labs Fleece Jacket")
    basket.expect_item_in_cart("Sauce Labs Bolt T-Shirt")

    basket_total = basket.get_items_total_price()

    checkout.open_checkout_page().fill_checkout_page_fake_data()

    checkout_total = checkout.get_item_total()
    assert checkout_total == basket_total, "Сумма товаров в Checkout не совпадает с корзиной"

    checkout.check_total_price().finish_checkout().check_success_message()


def test_checkout_without_postal_code(page):
    catalog = CatalogSteps(page)
    basket = BasketSteps(page)
    checkout = CheckoutSteps(page)

    catalog.login("standard_user", "secret_sauce")
    catalog.add_to_cart("Sauce Labs Fleece Jacket")

    basket.open_cart().expect_item_in_cart("Sauce Labs Fleece Jacket")

    checkout.open_checkout_page().fill_checkout_page(fake.first_name(), fake.last_name(), "")

    checkout.check_postal_code_error_message()
