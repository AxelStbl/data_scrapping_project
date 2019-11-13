import time
import datetime

from bs4 import BeautifulSoup
import urllib.request
from selenium import webdriver
from selenium.common.exceptions import ElementClickInterceptedException, NoSuchElementException, \
    StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup
import pandas as pd
import re
import os
import platform
from selenium.webdriver.firefox.options import Options

# We are using firefox headless with this option
HEADLESS = False
QUIT = True
SAVED_DATA = "saved_data"


# TODO maybe add chrome

def remove_sign_up_prompt(driver):
    """Method to remove sign up prompt from glassdoor so we won't have to login"""
    try:
        driver.find_element_by_class_name("selected").click()
    except ElementClickInterceptedException:
        pass

    driver.implicitly_wait(.1)

    try:
        driver.find_element_by_class_name("ModalStyle__xBtn___29PT9").click()  # clicking the X
    except NoSuchElementException:
        pass


def scrape_data_company(driver, elt, click=True):
    """Will click on the company name and each category so we can then store data"""
    # TODO move this when calling the function
    if click:
        elt.click()

    time.sleep(2)
    remove_sign_up_prompt(driver)
    tabs_category = driver.find_element_by_class_name("scrollableTabs")
    tabs_category = tabs_category.find_elements_by_class_name("tab")
    for tab in tabs_category:
        tab.click()
        name_category = tab.text
        print(name_category)
        time.sleep(.1)
        detail_tab = driver.find_element_by_class_name("jobDetailsInfoWrap")
        html_detail_tab = detail_tab.get_attribute('innerHTML')
        print(html_detail_tab)
        name_saved_data = name_category + ".html"
        with open(name_saved_data, 'a+') as f:
            f.write(html_detail_tab)

        # TODO store results of each click to a file
    # And click on each needed category if present
    # Then store the job offer
    # maybe just store the specific content like the data we want to store after BS traitment


def create_output_folder():
    """create output folder with saved data from glassdoor"""
    if not os.path.lexists(SAVED_DATA):
        os.mkdir(SAVED_DATA)
    os.chdir(SAVED_DATA)
    data_dir_by_date = datetime.datetime.now().strftime("data-%d-%b_%H:%M")
    os.mkdir(data_dir_by_date)
    os.chdir(data_dir_by_date)


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

    create_output_folder()

    init_job_page(base_url, driver)

    scrap_data_companies(driver)

    if QUIT:  # not quitting for debugging purposes
        driver.quit()
    pass


def get_job_id(html_job_container):
    """find the id of the job from the html container"""
    match = re.search(r'data-job-id="(\d*)"', html_job_container)
    if match:
        return match.group(1)


def get_name_company(html_job_container):
    """find the job name from html"""
    lines = html_job_container.splitlines()
    if len(lines) > 0:
        return lines[0]


def scrap_data_companies(driver):
    list_element = driver.find_elements_by_class_name("jobContainer")
    for i, elt in enumerate(list_element):
        click = True
        if i == 0:
            click = False  # We don't need to click on the first link since we are already seeing it
        remove_sign_up_prompt(driver)
        html_job_container = elt.get_attribute('innerHTML')
        time.sleep(2)
        name_company = get_name_company(elt.text)
        job_id = get_job_id(html_job_container)
        company_and_id_job = name_company + "-" + job_id
        os.mkdir(company_and_id_job)
        os.chdir(company_and_id_job)
        scrape_data_company(driver, elt, click)
        os.chdir("..")


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

# FIXME not working
# ignored_exceptions = (NoSuchElementException, StaleElementReferenceException,)
# tabs_category = WebDriverWait(driver, 4, ignored_exceptions=ignored_exceptions) \
#   .until(expected_conditions.presence_of_element_located((By.CLASS_NAME, "scrollableTabs")))
# tabs_category = WebDriverWait(tabs_category, 4, ignored_exceptions=ignored_exceptions) \
#   .until(expected_conditions.presence_of_all_elements_located((By.CLASS_NAME, "tab")))
