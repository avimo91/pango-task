from configuration.config import ADMIN_USERNAME, ADMIN_PASSWORD
from page_objects.login_page import LoginPage
from page_objects.dashboard_page import DashboardPage

class ParkingWorkflows:
    def __init__(self, driver):
        self.login_page = LoginPage(driver)
        self.dashboard_page = DashboardPage(driver)

    def login_as_admin(self) -> None:
        self.login_page.open()
        self.login_page.login(ADMIN_USERNAME, ADMIN_PASSWORD)

    def start_parking_session(self, plate: str, slot: str) -> None:
        self.dashboard_page.start_parking(plate, slot)