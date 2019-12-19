# All config here that can be tuned
# importing module
import logging
import os
import platform

from selenium import webdriver
from selenium.webdriver.firefox.options import Options

# DATABASE CONNECTION
USERNAME = "username"
PASSWORD = "password"
HOST = "localhost"
AUTH_PLUGIN = 'mysql_native_password'
SCRIPT_CREATION = 'database_creation.sql'

# We are using firefox headless with this option
HEADLESS = True
QUIT = True
SAVED_DATA = "saved_data"
SAVE_HTML_TO_FILE = True

RECAP = True  # Display all the job offers again at the end of the program
WAITING_TIME = 1  # in seconds depending of your connexion
JOB = 'Software Engineer'
BASE_URL = "https://www.glassdoor.com/Job/jobs.htm?locT=C&locId=" \
           "2421090&locKeyword=Tel%20Aviv&sc.keyword="
LOGGING_LEVEL = logging.ERROR

# API CALLS:
WIKIPEDIA_URL = 'https://en.wikipedia.org/api/rest_v1/page/summary/{}'
REST_COUNTRIES_EU = 'https://restcountries.eu/rest/v2/name/{}?fullText=true'


# website urls
def url_job():
    return BASE_URL + JOB


# Create and configure logger
def configure_logger():
    logging.basicConfig(filename="log_scrapping.log",
                        format='%(asctime)s %(message)s',
                        filemode='w')

    # Creating an object
    logger = logging.getLogger()

    # Setting the threshold of logger to DEBUG
    logger.setLevel(LOGGING_LEVEL)
    return logger


def get_geckodriver():
    """We have included the geckodriver for firefox for windows mac and
    linux
    :return: appropriate driver based on the os launching the app """
    running_system = platform.system()
    driver = None
    options = Options()
    options.headless = HEADLESS
    if os.getcwd().endswith("scrapping"):
        executable_path = "drivers"
    else:
        executable_path = os.path.join("scrapping", "drivers")

    if running_system == "Linux":
        executable_path = os.path.join(executable_path,
                                       "geckodriver-linux", "geckodriver")
    elif running_system == "Darwin":
        executable_path = os.path.join(executable_path,
                                       "geckodriver-macos", "geckodriver")
    elif running_system == "Windows":
        executable_path = os.path.join(executable_path,
                                       "geckodriver-win", "geckodriver")
    else:
        print(
            "You don't have a compatible operating system for running this "
            "scrapper")
    if executable_path != "":
        driver = webdriver.Firefox(options=options,
                                   executable_path=executable_path)
    return driver

