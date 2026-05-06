from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class CheckoutPage:
    _FIRST_NAME = (By.ID, "first-name")
    _LAST_NAME = (By.ID, "last-name")
    _ZIP_CODE = (By.ID, "postal-code")
    _CONTINUE_BTN = (By.ID, "continue")
    _FINISH_BTN = (By.ID, "finish")
    _CONFIRMATION = (By.CLASS_NAME, "complete-header")
    _WAIT_TIMEOUT = 15

    def __init__(self, driver: WebDriver):
        self._driver = driver
        self._wait = WebDriverWait(driver, self._WAIT_TIMEOUT)

    def fill_shipping_info(self, first: str, last: str, zip_code: str) -> None:
        self._wait.until(EC.element_to_be_clickable(self._FIRST_NAME)).send_keys(first)
        self._wait.until(EC.element_to_be_clickable(self._LAST_NAME)).send_keys(last)
        self._wait.until(EC.element_to_be_clickable(self._ZIP_CODE)).send_keys(zip_code)
        self._driver.find_element(By.TAG_NAME, "form").submit()
        self._wait.until(EC.url_contains("checkout-step-two.html"))

    def finish_order(self) -> None:
        finish_button = self._wait.until(EC.element_to_be_clickable(self._FINISH_BTN))
        self._driver.execute_script("arguments[0].click();", finish_button)
        self._wait.until(EC.url_contains("checkout-complete"))

    def get_confirmation_message(self) -> str:
        return self._wait.until(
            EC.presence_of_element_located(self._CONFIRMATION)
        ).text
