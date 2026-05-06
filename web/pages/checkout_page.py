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

    def _react_fill(self, locator: tuple, value: str) -> None:
        el = self._wait.until(EC.presence_of_element_located(locator))
        self._driver.execute_script(
            """
            var setter = Object.getOwnPropertyDescriptor(
                window.HTMLInputElement.prototype, 'value').set;
            setter.call(arguments[0], arguments[1]);
            arguments[0].dispatchEvent(new Event('input', {bubbles: true}));
            arguments[0].dispatchEvent(new Event('change', {bubbles: true}));
            """,
            el,
            value,
        )

    def fill_shipping_info(self, first: str, last: str, zip_code: str) -> None:
        self._wait.until(EC.presence_of_element_located(self._FIRST_NAME))
        self._react_fill(self._FIRST_NAME, first)
        self._react_fill(self._LAST_NAME, last)
        self._react_fill(self._ZIP_CODE, zip_code)
        btn = self._wait.until(EC.element_to_be_clickable(self._CONTINUE_BTN))
        self._driver.execute_script("arguments[0].scrollIntoView(true);", btn)
        btn.click()
        self._wait.until(EC.url_contains("checkout-step-two.html"))

    def finish_order(self) -> None:
        finish_button = self._wait.until(EC.element_to_be_clickable(self._FINISH_BTN))
        self._driver.execute_script("arguments[0].click();", finish_button)
        self._wait.until(EC.url_contains("checkout-complete"))

    def get_confirmation_message(self) -> str:
        return self._wait.until(
            EC.presence_of_element_located(self._CONFIRMATION)
        ).text
