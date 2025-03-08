import os
import shutil

import pytest
from pytest_html import extras

from constants import REPORT_DIR
from helpers.env_helper import EnvHelper
from utils.base_config import BaseConfig
from utils.custom_log import CustomLog
from web_driver_config.web_driver_config import WebDriverConfig

c_logger = CustomLog.log_gen()


@pytest.hookimpl(tryfirst=True)
def pytest_configure(config):
    pytest.driver = None
    pytest.config_obj = config
    _create_reports_folder()


@pytest.fixture(scope='class')
def t_config(request, cmd_options):

    browser = cmd_options["browser"]
    browser_instance = WebDriverConfig().get_browser_instance(browser)
    request.cls.driver = browser_instance
    pytest.driver = browser_instance
    cfg = BaseConfig()
    cfg.env = cmd_options["env"]
    cfg.driver = browser_instance
    cfg.url = EnvHelper.url_resolver(cfg.env)
    yield cfg
    browser_instance.quit()
    pytest.driver = None


def pytest_addoption(parser):
    parser.addoption("-E", "--env", help="Environment: prod")
    parser.addoption("-B", "--browser", help="Browsers: chrome | firefox")


@pytest.fixture(scope="session")
def cmd_options(request):
    cmd_options = dict()
    cmd_options["env"] = request.config.getoption("--env")
    cmd_options["browser"] = request.config.getoption("--browser")
    _validate_cmd_options(cmd_options)
    return cmd_options


def _validate_cmd_options(cmd_options):
    env_type = cmd_options["env"]
    env_types = ["prod"]
    if env_type not in env_types:
        raise ValueError(f"Invalid environment. Allowed values are {env_types}")
    browser = cmd_options["browser"]
    browsers = ["chrome", "firefox"]
    if browser not in browsers:
        raise ValueError(f"Invalid browser. Allowed values are {browsers}")


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item):
    outcome = yield
    report = outcome.get_result()

    if report.when in ("setup", "call"):
        if report.failed:
            test_name = item.originalname
            _capture_screenshot_and_add_to_report(test_name, report)


def _capture_screenshot_and_add_to_report(test_name, report):
    """ Captures screenshot for failing test and attaches it to the report
    Args:
        test_name: name of the test
    """
    pytest.driver.save_screenshot(f"{REPORT_DIR}/{test_name}.png")
    report.extra = [extras.image(f"file:{test_name}.png")]


def _create_reports_folder():
    """Deletes if directory exists and creates a fresh one"""
    try:
        if os.path.isdir(REPORT_DIR):
            shutil.rmtree(REPORT_DIR)
        os.mkdir(REPORT_DIR)
    except OSError as e:
        raise OSError(f"Error while creating reports directory - {e}.")
