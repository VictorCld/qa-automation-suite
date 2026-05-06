import os
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

_URL = os.getenv("SAUCE_URL", "https://www.saucedemo.com")
_WAIT_TIMEOUT = 15


class LoginPage:
    _USERNAME = (By.ID, "user-name")
    _PASSWORD = (By.ID, "password")
    _LOGIN_BTN = (By.ID, "login-button")

    def __init__(self, driver: WebDriver):
        self._driver = driver
        self._wait = WebDriverWait(driver, _WAIT_TIMEOUT)

    def open(self) -> None:
        self._driver.get(_URL)

    def login(self, username: str, password: str) -> None:
        self._wait.until(EC.element_to_be_clickable(self._USERNAME)).send_keys(username)
        self._driver.find_element(*self._PASSWORD).send_keys(password)
        self._wait.until(EC.element_to_be_clickable(self._LOGIN_BTN)).click()
