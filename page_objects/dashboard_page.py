from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from page_objects.base_page import BasePage

class DashboardPage(BasePage):
    CAR_PLATE_INPUT = (By.ID, "car_plate")
    SLOT_INPUT = (By.ID, "slot")
    START_PARKING_BUTTON = (By.ID, "submit")
    ACTIVE_TABLE_ROWS = (By.CSS_SELECTOR, "table tbody tr")
    PLATE_INVALID_FIELD = (By.CSS_SELECTOR, "#car_plate.is-invalid")

    def start_parking(self, plate: str, slot: str) -> None:
        self.actions.type(self.CAR_PLATE_INPUT, plate)
        self.actions.type(self.SLOT_INPUT, slot)
        self.actions.click(self.START_PARKING_BUTTON)

    def is_plate_in_active_table(self, plate: str) -> bool:
        try:
            self.actions.wait.until(
                lambda driver: any(
                    plate in row.text
                    for row in driver.find_elements(*self.ACTIVE_TABLE_ROWS)
                )
            )
            return True
        except Exception:
            return False

    def is_plate_invalid_state_visible(self) -> bool:
        try:
            return self.actions.wait.until(
                EC.visibility_of_element_located(self.PLATE_INVALID_FIELD)
            ).is_displayed()
        except Exception:
            return False