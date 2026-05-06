import os
import pytest
from web.pages.login_page import LoginPage
from web.pages.inventory_page import InventoryPage
from web.pages.cart_page import CartPage
from web.pages.checkout_page import CheckoutPage
from web.utils.driver_factory import create_driver

_USER = os.getenv("SAUCE_USER", "standard_user")
_PASSWORD = os.getenv("SAUCE_PASSWORD", "secret_sauce")
_PRODUCTS = ["Sauce Labs Backpack", "Sauce Labs Bike Light"]


@pytest.fixture
def driver():
    d = create_driver()
    yield d
    d.quit()


@pytest.mark.web
class TestCheckoutE2E:
    def test_login_navigates_to_inventory(self, driver):
        login = LoginPage(driver)
        login.open()
        login.login(_USER, _PASSWORD)
        assert "inventory" in driver.current_url

    def test_add_products_appear_in_cart(self, driver):
        login = LoginPage(driver)
        login.open()
        login.login(_USER, _PASSWORD)

        inventory = InventoryPage(driver)
        for product in _PRODUCTS:
            inventory.add_product_to_cart(product)
        inventory.go_to_cart()

        cart = CartPage(driver)
        items = cart.get_item_names()
        assert "Sauce Labs Backpack" in items
        assert "Sauce Labs Bike Light" in items

    def test_complete_checkout_shows_confirmation(self, driver):
        login = LoginPage(driver)
        login.open()
        login.login(_USER, _PASSWORD)

        inventory = InventoryPage(driver)
        for product in _PRODUCTS:
            inventory.add_product_to_cart(product)
        inventory.go_to_cart()

        cart = CartPage(driver)
        cart.proceed_to_checkout()

        checkout = CheckoutPage(driver)
        checkout.fill_shipping_info("Test", "User", "12345")
        checkout.finish_order()

        assert checkout.get_confirmation_message() == "Thank you for your order!"
