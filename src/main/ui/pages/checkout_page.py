from faker import Faker

from playwright.sync_api import Page, expect

from src.main.ui.utils.constants import Urls

fake = Faker()


class CheckoutPage:
    def __init__(self, page: Page):
        self.page = page
        self.first_name_input = page.get_by_placeholder("First Name")
        self.last_name_input = page.get_by_placeholder("Last Name")
        self.postal_code_input = page.get_by_placeholder("Zip/Postal Code")

        self.continue_button = page.locator("data-test=continue")
        self.cancel_button = page.locator("data-test=cancel")
        self.finish_button = page.locator("data-test=finish")
        self.menu_button = page.locator("#react-burger-menu-btn")
        self.back_home_button = page.locator("data-test=back-to-products")
        self.checkout_button = page.locator("data-test=checkout")
        self.logout_link = page.locator("#logout_sidebar_link")

        self.item_total_price = page.locator('[data-test="subtotal-label"]')
        self.tax = page.locator('[data-test="tax-label"]')
        self.total_price = page.locator('[data-test="total-label"]')

        self.success_message = page.locator(".complete-header")
        self.error_message = page.locator('[data-test="error"]')

    def open_checkout(self):
        self.checkout_button.click()
        expect(self.page).to_have_url(Urls.CHECKOUT_STEP_ONE)

    def fill_credentials_with_fake_data_and_continue(self):
        expect(self.first_name_input).to_be_visible()

        first_name, last_name, postal_code = fake.first_name(), fake.last_name(), fake.postalcode()

        self.first_name_input.fill(first_name)
        self.last_name_input.fill(last_name)
        self.postal_code_input.fill(postal_code)

        self.continue_button.click()
        expect(self.page).to_have_url(Urls.CHECKOUT_STEP_TWO)
        return {
            "first_name": first_name,
            "last_name": last_name,
            "postal_code": postal_code
        }

    def fill_credentials_and_continue(self, first_name: str, last_name: str, postal_code: str):
        self.first_name_input.fill(first_name)
        self.last_name_input.fill(last_name)
        self.postal_code_input.fill(postal_code)
        self.continue_button.click()

    def finish_checkout(self):
        self.finish_button.click()
        expect(self.page).to_have_url(Urls.CHECKOUT_COMPLETE)

    def get_item_total_price(self) -> float:
        expect(self.item_total_price).to_be_visible()
        item_total_text = self.item_total_price.inner_text()
        item_total_value = float(item_total_text.split("$")[1])
        return item_total_value

    def get_tax(self) -> float:
        expect(self.tax).to_be_visible()
        tax_text = self.tax.inner_text()
        tax_value = float(tax_text.split("$")[1])
        return tax_value

    def get_total_price(self) -> float:
        expect(self.total_price).to_be_visible()
        total_text = self.total_price.inner_text()
        total_value = float(total_text.split("$")[1])
        return total_value

    def get_success_message(self) -> str:
        expect(self.success_message).to_be_visible()
        return self.success_message.inner_text()

    def get_error_message(self) -> str:
        expect(self.error_message).to_be_visible()
        return self.error_message.inner_text()
