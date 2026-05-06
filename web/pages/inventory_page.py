from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

_WAIT_TIMEOUT = 15


class InventoryPage:
    _CART_LINK = (By.CLASS_NAME, "shopping_cart_link")
    _ITEMS = (By.CLASS_NAME, "inventory_item")
    _ITEM_NAME = (By.CLASS_NAME, "inventory_item_name")
    _INVENTORY_CONTAINER = (By.ID, "inventory_container")
    _REMOVE_BUTTON_XPATH = ".//button[normalize-space()='Remove']"

    def __init__(self, driver: WebDriver):
        self._driver = driver
        self._wait = WebDriverWait(driver, _WAIT_TIMEOUT)

    def add_product_to_cart(self, product_name: str) -> None:
        self._wait.until(EC.presence_of_element_located(self._INVENTORY_CONTAINER))
        for item in self._driver.find_elements(*self._ITEMS):
            if item.find_element(*self._ITEM_NAME).text == product_name:
                button = self._wait.until(
                    lambda _: item.find_element(By.TAG_NAME, "button")
                )
                self._driver.execute_script("arguments[0].click();", button)
                self._wait.until(
                    lambda _: item.find_elements(By.XPATH, self._REMOVE_BUTTON_XPATH)
                )
                return
        raise ValueError(f"Product '{product_name}' not found")

    def go_to_cart(self) -> None:
        element = self._wait.until(EC.element_to_be_clickable(self._CART_LINK))
        self._driver.execute_script("arguments[0].click();", element)
        self._wait.until(EC.url_contains("cart.html"))
