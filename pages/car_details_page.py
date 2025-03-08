from selenium.webdriver.common.by import By

from constants import GLOBAL_TIME_OUT
from pages.base_page import BasePage


class CarDetailsPage(BasePage):
    """This class contains element locators in Car Details Page
    Page: https://motor.confused.com/ -> Car Details Page
    """

    def __init__(self, driver, time_out=GLOBAL_TIME_OUT):
        super().__init__(driver, time_out)

        self.input_txt_ENTER_CAR_REGISTRATION = {"locator": (By.ID, "registration-number-input"),
                                                 "name": "Enter car registration"}
        self.btn_FIND_CAR = {"locator": (By.ID, "find-vehicle-btn"),
                             "name": "Find car"}
        self.ro_txt_VEHICLE_SUMMARY = {"locator": (By.CSS_SELECTOR, "#vehicle-summary .panel"),
                                       "name": "Vehicle Summary"}
        self.ro_txt_REGISTRATION = {"locator": (By.CSS_SELECTOR, "#vehicle-summary .panel p:nth-of-type(1) b"),
                                    "name": "Vehicle Registration"}
        self.ro_txt_MANUFACTURER = {"locator": (By.CSS_SELECTOR, "#vehicle-summary .panel p:nth-of-type(2) b"),
                                    "name": "Vehicle Manufacturer"}
        self.ro_txt_YEAR = {"locator": (By.CSS_SELECTOR, "#vehicle-summary .panel p:nth-of-type(5) b"),
                            "name": "Vehicle Manufacturer"}
        self.btn_CHANGE_VEHICLE = {"locator": (By.ID, "change-vehicle-btn"),
                                   "name": "Change Vehicle"}
        self.ro_txt_VEHICLE_NOT_FOUND = {"locator": (By.ID, "vehicle-error-container"),
                                         "name": "Vehicle not found error message"}
        self.btn_FEEDBACK = {"locator": (By.ID, "saberfeedback_button"),
                             "name": "Feedback"}
