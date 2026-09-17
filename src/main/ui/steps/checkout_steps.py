import allure
import pytest
from playwright.sync_api import Page, expect

from src.main.ui.pages.checkout_page import CheckoutPage


class CheckoutSteps:
    def __init__(self, page: Page):
        self.page = page
        self.checkout_page = CheckoutPage(page)

    @allure.step("Open checkout page")
    def open_checkout_page(self):
        self.checkout_page.open_checkout()
        return self

    @allure.step("Fill credentials with fake data and continue")
    def fill_checkout_page_fake_data(self):
        self.checkout_page.fill_credentials_with_fake_data_and_continue()
        return self

    @allure.step("Open checkout page")
    def fill_checkout_page(self, first_name: str, last_name: str, zip_code: str):
        self.checkout_page.fill_credentials_and_continue(first_name, last_name, zip_code)
        return self

    @allure.step("Get item total in checkout page")
    def get_item_total(self):
        return self.checkout_page.get_item_total_price()

    @allure.step("Get tax in checkout page")
    def get_tax(self):
        return self.checkout_page.get_tax()

    @allure.step("Get total in chechout page")
    def get_total(self):
        return self.checkout_page.get_total_price()

    @allure.step("Check if item total + tax is equal to total price")
    def check_total_price(self):
        assert pytest.approx(self.get_item_total() + self.get_tax(),
                             0.01) == self.get_total(), f"Expected total {self.get_item_total() + self.get_tax()}, but got {self.get_total()}"
        return self

    @allure.step("Finish checkout page")
    def finish_checkout(self):
        self.checkout_page.finish_checkout()
        return self

    @allure.step("Check success message")
    def check_success_message(self):
        assert "Thank you for your order!" == self.checkout_page.get_success_message()
        return self

    @allure.step("Expect error message: Postal Code is required")
    def check_postal_code_error_message(self):
        assert "Error: Postal Code is required" == self.checkout_page.get_error_message()
        return self
