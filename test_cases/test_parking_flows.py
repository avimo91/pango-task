import pytest
from workflows.parking_workflows import ParkingWorkflows
from page_objects.dashboard_page import DashboardPage
from utils.data_generator import generate_plate, generate_slot
from configuration.config import INVALID_PLATE_DATA


@pytest.fixture
def workflow(driver):
    return ParkingWorkflows(driver)


@pytest.fixture
def dashboard(driver):
    return DashboardPage(driver)



def test_start_parking_appears_in_active_table(workflow, dashboard):
    plate = generate_plate()

    workflow.login_as_admin()
    workflow.start_parking_session(plate, generate_slot())

    assert dashboard.is_plate_in_active_table(plate)


def test_invalid_plate_shows_validation_error(workflow, dashboard):
    workflow.login_as_admin()
    workflow.start_parking_session(INVALID_PLATE_DATA, generate_slot())

    assert dashboard.is_plate_invalid_state_visible()