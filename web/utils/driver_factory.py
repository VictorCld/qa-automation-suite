import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def create_driver() -> webdriver.Chrome:
    options = Options()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    if os.getenv("HEADLESS", "true").lower() == "true":
        options.add_argument("--headless=new")
    return webdriver.Chrome(options=options)
