import os
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

_URL = os.getenv("SAUCE_URL", "https://www.saucedemo.com")


class LoginPage:
    _USERNAME = (By.ID, "user-name")
    _PASSWORD = (By.ID, "password")
    _LOGIN_BTN = (By.ID, "login-button")

    def __init__(self, driver: WebDriver):
        self._driver = driver

    def open(self) -> None:
        self._driver.get(_URL)

    def login(self, username: str, password: str) -> None:
        self._driver.find_element(*self._USERNAME).send_keys(username)
        self._driver.find_element(*self._PASSWORD).send_keys(password)
        self._driver.find_element(*self._LOGIN_BTN).click()
