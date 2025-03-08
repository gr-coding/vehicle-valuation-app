from selenium.common import TimeoutException, NoSuchElementException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec


class BasePage:
    """BasePage class - This parent class contains common methods that can be inherited by all the child pages"""

    def __init__(self, driver, time_out):
        self.driver = driver
        self.time_out = time_out
        self.driver.implicitly_wait(time_out)

    def click(self, locator_data, time_out=None):
        """ Performs click on a given element
        Args:
            locator_data : dictionary containing the element's locator and related data
            time_out : value in seconds overriding the default TIMEOUT
        Returns:
            True -if successful
        Raises:
            BasePageException: If the click fails or if the locator key is invalid
        """
        if time_out is None:
            time_out = self.time_out

        try:
            locator = locator_data["locator"]
            WebDriverWait(self.driver, time_out).until(ec.element_to_be_clickable(locator)).click()
            return True
        except TimeoutException:
            raise BasePageException("BasePage: click - TimeoutException: unable to click on the element.")
        except KeyError:
            raise BasePageException("BasePage: click -Invalid locator key")

    def clear_and_fill_in_field(self, locator_data, text, time_out=None):
        """ Clears and fills the provided string value in an input element
        Args:
            locator_data : dictionary containing the element's locator and related data
            text : text to be filled in
            time_out : value in seconds overriding the default TIMEOUT
        Returns:
            True -if successful
        Raises:
            BasePageException: If the fill in text field operation fails or if the locator key is invalid
        """
        if time_out is None:
            time_out = self.time_out

        try:
            locator = locator_data["locator"]
            WebDriverWait(self.driver, time_out).until(ec.element_to_be_clickable(locator)).clear()
            WebDriverWait(self.driver, time_out).until(ec.element_to_be_clickable(locator)).send_keys(text)
            return True
        except TimeoutException:
            raise BasePageException(
                "BasePage: clear_and_fill_in_field - TimeoutException: unable to click on the element.")
        except KeyError:
            raise BasePageException("BasePage: clear_and_fill_in_field -Invalid locator key")

    def get_text(self, locator_data, time_out=None):
        """ Returns the text of an element
        Args:
            locator_data : dictionary containing the element's locator and related data
            time_out : value in seconds overriding the default TIMEOUT
        Returns:
            Element's text
        Raises:
            BasePageException: If the locator key is invalid
        """
        if time_out is None:
            time_out = self.time_out

        try:
            locator = locator_data["locator"]
            return WebDriverWait(self.driver, time_out).until(ec.visibility_of_element_located(locator)).text
        except TimeoutException:
            raise BasePageException("BasePage: get_text - TimeoutException while checking the element's text")
        except KeyError:
            raise BasePageException("BasePage: get_text -Invalid locator key")

    def wait_until_text_to_be_present(self, locator_data, text, time_out=None):
        if time_out is None:
            time_out = self.time_out
        try:
            locator = locator_data["locator"]
            return WebDriverWait(self.driver, time_out).until(ec.text_to_be_present_in_element(locator, text))
        except TimeoutException:
            raise BasePageException(
                "BasePage: wait_until_text_to_be_present - TimeoutException while checking the element's text")
        except KeyError:
            raise BasePageException("BasePage: wait_until_text_to_be_present -Invalid locator key")

    def is_element_displayed(self, locator_data):
        """ Returns if the given element is displayed
        Args:
            locator_data : dictionary containing the element's locator and related data
        Returns:
            True or False based on element's display state
        Raises:
            BasePageException: If the locator key is invalid
        """
        try:
            locator = locator_data["locator"]
            el = self.driver.find_element(*locator)
            return el.is_displayed()
        except NoSuchElementException:
            return False
        except KeyError:
            raise BasePageException("BasePage: is_element_displayed -Invalid locator key")


class BasePageException(Exception):
    """Exception class for BasePage"""
    pass
