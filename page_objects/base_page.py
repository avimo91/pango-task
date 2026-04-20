from configuration.config import DEFAULT_TIMEOUT
from extensions.ui_actions import UIActions

class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.actions = UIActions(driver, timeout=DEFAULT_TIMEOUT)

    def open_url(self, url: str) -> None:
        self.driver.get(url)