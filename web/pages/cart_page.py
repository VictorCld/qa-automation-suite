from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver


class CartPage:
    _ITEM_NAMES = (By.CLASS_NAME, "inventory_item_name")
    _CHECKOUT_BTN = (By.ID, "checkout")

    def __init__(self, driver: WebDriver):
        self._driver = driver

    def get_item_names(self) -> list[str]:
        return [el.text for el in self._driver.find_elements(*self._ITEM_NAMES)]

    def proceed_to_checkout(self) -> None:
        self._driver.find_element(*self._CHECKOUT_BTN).click()
