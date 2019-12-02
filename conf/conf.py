# All config here that can be tuned
# importing module
import logging
import os
import platform

from selenium import webdriver
from selenium.webdriver.firefox.options import Options

# We are using firefox headless with this option
HEADLESS = False
QUIT = True
SAVED_DATA = "saved_data"
RECAP = True  # Display all the job offers again at the end of the program
WAITING_TIME = 1  # in seconds depending of your connexion

# website urls
BASE_URL = "https://www.glassdoor.com/Job/tel-aviv-software-engineer-jobs" \
           "-SRCH_IL.0,8_IC2421090_KO9,26.htm "

date_path = ""
current_path = ""


# Create and configure logger
def configure_logger():
    logging.basicConfig(filename="log_scrapping.log",
                        format='%(asctime)s %(message)s',
                        filemode='w')

    # Creating an object
    logger = logging.getLogger()

    # Setting the threshold of logger to DEBUG
    logger.setLevel(logging.ERROR)
    return logger


def get_geckodriver():
    """We have included the geckodriver for firefox for windows mac and
    linux
    :return: appropriate driver based on the os launching the app """
    running_system = platform.system()
    driver = None
    options = Options()
    options.headless = HEADLESS
    executable_path = os.path.join("..", "drivers")
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
