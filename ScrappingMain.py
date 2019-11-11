import time

from bs4 import BeautifulSoup
import urllib.request
from selenium import webdriver
from selenium.common.exceptions import ElementClickInterceptedException, NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup
import pandas as pd
import re
import os
import platform
from selenium.webdriver.firefox.options import Options

HEADLESS = False
QUIT = True


def remove_sign_up_prompt(driver):
    try:
        driver.find_element_by_class_name("selected").click()
    except ElementClickInterceptedException:
        pass

    driver.implicitly_wait(.1)

    try:
        driver.find_element_by_class_name("ModalStyle__xBtn___29PT9").click()  # clicking the X
    except NoSuchElementException:
        pass


def main():
    """Main function launch our functions"""

    # website urls
    base_url = "https://www.glassdoor.com/Job/tel-aviv-software-engineer-jobs-SRCH_IL.0,8_IC2421090_KO9,26.htm"

    # Firefox session

    # Chooses the right executable
    driver = get_geckodriver()
    if not driver:
        print("Driver not found for your operating system")
        return

    init_job_page(base_url, driver)

    list_element = driver.find_elements_by_class_name("jobEmpolyerName")
    print(list_element)
    for elt in list_element:
        remove_sign_up_prompt(driver)
        name_company = elt.text
        print(name_company)
        elt.click()
        time.sleep(2)

    ## TODO store results of each click to a file
    ## And click on each needed category if present
    ## Then store the job offer

    text = driver.page_source
    f = open("test.html", 'a+')
    f.write(text)
    f.close()
    if QUIT:  # not quitting for debugging purposes
        driver.quit()
    pass


def init_job_page(base_url, driver):
    driver.get(base_url)
    driver.implicitly_wait(100)


def get_geckodriver():
    running_system = platform.system()
    driver = None
    options = Options()
    options.headless = HEADLESS
    executable_path = ""
    if running_system == "Linux":
        executable_path = r'./geckodriver-linux/geckodriver'
    elif running_system == "Darwin":
        executable_path = r'./geckodriver-macos/geckodriver'
    elif running_system == "Windows":
        executable_path = r'./geckodriver-win/geckodriver'
    else:
        print("You don't have a compatible operating system for running this scrapper")
    if executable_path != "":
        driver = webdriver.Firefox(options=options, executable_path=executable_path)
    return driver


if __name__ == '__main__':
    main()
