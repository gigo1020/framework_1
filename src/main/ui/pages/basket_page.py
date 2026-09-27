from playwright.sync_api import Page, expect

from src.main.ui.utils.constants import Urls


class BasketPage:
    def __init__(self, page: Page):
        self.page = page
        self.product_cards = page.locator(".cart_item_label")
        self.menu_button = page.locator("#react-burger-menu-btn")
        self.checkout_button = page.get_by_role("button", name="Checkout")
        self.logout_link = page.get_by_role("button", name="Logout")

    def open_cart(self):
        self.page.goto(Urls.CART)

    def logout(self):
        self.menu_button.click()
        self.logout_link.click()

    def checkout(self):
        self.checkout_button.click()
        expect(self.page).to_have_url(Urls.CHECKOUT_STEP_ONE)

    def remove_from_cart(self, product_name: str):
        card = self.product_cards.filter(has_text=product_name)
        remove_button = card.locator("button")
        remove_button.click()

    def get_item_names(self) -> list[str]:
        try:
            expect(self.product_cards.first).to_be_visible(timeout=2000)
            return self.product_cards.locator(".inventory_item_name").all_text_contents()
        except:
            return []

    def get_items_total_price(self) -> list[float]:
        try:
            expect(self.product_cards.first).to_be_visible()
            prices_text = self.product_cards.locator(".inventory_item_price").all_text_contents()
            return [float(p.replace("$", "")) for p in prices_text]
        except:
            return []
