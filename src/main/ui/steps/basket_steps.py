import allure
from playwright.sync_api import Page

from src.main.ui.pages.basket_page import BasketPage


class BasketSteps:
    BASKET_URL = "https://www.saucedemo.com/cart.html"

    def __init__(self, page: Page):
        self.page = page
        self.basket_page = BasketPage(page)

    @allure.step("Open cart page")
    def open_cart(self):
        self.basket_page.open_cart()
        return self

    @allure.step("Get list of items in cart")
    def get_item_names(self) -> list:
        try:
            return self.basket_page.get_item_names()
        except:
            return []

    @allure.step("Check if the {item} is in cart")
    def expect_item_in_cart(self, item: str):
        assert item in self.get_item_names()
        return self

    @allure.step("Check if the item is not in cart")
    def expect_item_not_in_cart(self, item: str):
        assert item not in self.get_item_names()
        return self

    @allure.step("Remove from cart")
    def remove_from_cart(self, item: str):
        self.basket_page.remove_from_cart(item)
        return self

    @allure.step("Checkout in cart")
    def checkout(self):
        self.basket_page.checkout()
        return self

    @allure.step("Get items total price")
    def get_items_total_price(self):
        return sum(self.basket_page.get_items_total_price())
