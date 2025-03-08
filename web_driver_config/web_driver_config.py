from selenium import webdriver


class WebDriverConfig:

    @staticmethod
    def _create_web_driver(browser):
        """
        Initializes and returns webdriver instance
        Args:
            browser: name of the browser -  chrome|firefox
        Returns:
            Webdriver instance
        """
        browser_instance = None
        browser = browser.lower()

        if browser == "chrome":
            options = webdriver.ChromeOptions()
            browser_instance = webdriver.Chrome(options=options)
        elif browser == "firefox":
            options = webdriver.FirefoxOptions()
            browser_instance = webdriver.Firefox(options=options)
        return browser_instance

    def get_browser_instance(self, browser):
        """
        Initializes and returns a Webdriver instance for the specified browser
        Args:
            browser:name of the browser -  chrome|firefox
        Returns:
            Webdriver instance
        """
        browser_instance = self._create_web_driver(browser)
        browser_instance.maximize_window()
        return browser_instance
