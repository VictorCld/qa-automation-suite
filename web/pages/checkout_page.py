from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver


class CheckoutPage:
    _FIRST_NAME = (By.ID, "first-name")
    _LAST_NAME = (By.ID, "last-name")
    _ZIP_CODE = (By.ID, "postal-code")
    _CONTINUE_BTN = (By.ID, "continue")
    _FINISH_BTN = (By.ID, "finish")
    _CONFIRMATION = (By.CLASS_NAME, "complete-header")

    def __init__(self, driver: WebDriver):
        self._driver = driver

    def fill_shipping_info(self, first: str, last: str, zip_code: str) -> None:
        self._driver.find_element(*self._FIRST_NAME).send_keys(first)
        self._driver.find_element(*self._LAST_NAME).send_keys(last)
        self._driver.find_element(*self._ZIP_CODE).send_keys(zip_code)
        self._driver.find_element(*self._CONTINUE_BTN).click()

    def finish_order(self) -> None:
        self._driver.find_element(*self._FINISH_BTN).click()

    def get_confirmation_message(self) -> str:
        return self._driver.find_element(*self._CONFIRMATION).text
