import os
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from selenium import webdriver


def create_driver() -> "webdriver.Chrome":
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options

    options = Options()
    options.add_experimental_option(
        "prefs",
        {
            "autofill.credit_card_enabled": False,
            "autofill.profile_enabled": False,
            "credentials_enable_service": False,
            "profile.default_content_setting_values.geolocation": 2,
            "profile.default_content_setting_values.media_stream_camera": 2,
            "profile.default_content_setting_values.media_stream_mic": 2,
            "profile.default_content_setting_values.notifications": 2,
            "profile.default_content_settings.popups": 0,
            "profile.password_manager_leak_detection": False,
            "profile.password_manager_enabled": False,
        },
    )
    options.set_capability("unhandledPromptBehavior", "dismiss")
    options.add_argument(
        "--disable-features="
        "AutofillServerCommunication,"
        "PasswordGeneration,"
        "PasswordLeakDetection,"
        "PasswordManagerEnabled,"
        "PasswordManagerOnboarding"
    )
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-notifications")
    options.add_argument("--window-size=1920,1080")
    if os.getenv("HEADLESS", "true").lower() == "true":
        options.add_argument("--headless=new")
    return webdriver.Chrome(options=options)
