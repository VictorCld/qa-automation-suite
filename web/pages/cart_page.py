from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

_WAIT_TIMEOUT = 15


class CartPage:
    _ITEM_NAMES = (By.CLASS_NAME, "inventory_item_name")
    _CHECKOUT_BTN = (By.ID, "checkout")
    _CART_CONTENTS = (By.CLASS_NAME, "cart_contents_container")

    def __init__(self, driver: WebDriver):
        self._driver = driver
        self._wait = WebDriverWait(driver, _WAIT_TIMEOUT)

    def get_item_names(self) -> list[str]:
        self._wait.until(EC.presence_of_element_located(self._CART_CONTENTS))
        return [el.text for el in self._driver.find_elements(*self._ITEM_NAMES)]

    def proceed_to_checkout(self) -> None:
        self._wait.until(EC.element_to_be_clickable(self._CHECKOUT_BTN)).click()
