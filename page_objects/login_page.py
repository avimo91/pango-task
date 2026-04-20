from selenium.webdriver.common.by import By
from configuration.config import LOGIN_URL
from page_objects.base_page import BasePage

class LoginPage(BasePage):
    USERNAME_INPUT = (By.ID, "username")
    PASSWORD_INPUT = (By.ID, "password")
    LOGIN_BUTTON = (By.CSS_SELECTOR, "button[type='submit']")

    def open(self) -> None:
        self.open_url(LOGIN_URL)

    def login(self, username: str, password: str) -> None:
        self.actions.type(self.USERNAME_INPUT, username)
        self.actions.type(self.PASSWORD_INPUT, password)
        self.actions.click(self.LOGIN_BUTTON)