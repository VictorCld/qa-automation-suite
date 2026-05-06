from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver


class InventoryPage:
    _CART_LINK = (By.CLASS_NAME, "shopping_cart_link")
    _ITEMS = (By.CLASS_NAME, "inventory_item")
    _ITEM_NAME = (By.CLASS_NAME, "inventory_item_name")

    def __init__(self, driver: WebDriver):
        self._driver = driver

    def add_product_to_cart(self, product_name: str) -> None:
        for item in self._driver.find_elements(*self._ITEMS):
            if item.find_element(*self._ITEM_NAME).text == product_name:
                item.find_element(By.TAG_NAME, "button").click()
                return
        raise ValueError(f"Product '{product_name}' not found")

    def go_to_cart(self) -> None:
        self._driver.find_element(*self._CART_LINK).click()
