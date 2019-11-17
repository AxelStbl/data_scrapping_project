import datetime
import logging
import os
import platform
import re
import time

from selenium import webdriver
from selenium.common.exceptions import ElementClickInterceptedException, NoSuchElementException, \
    ElementNotInteractableException
from selenium.webdriver.firefox.options import Options

# We are using firefox headless with this option
from Company import Company
from JobOffer import JobOffer, print_jobs
from TabScrapping import scrape_company_tab, rating, nbr_of_ratings, benefits_rate, nbr_of_benefits_rating

HEADLESS = True
QUIT = True
SAVED_DATA = "saved_data"
RECAP = True  # Display all the job offers again at the end of the program


def scrape_data_company(driver, elt, job, should_click=True):
    """Will click on the company name and each category so we can then store data"""
    if should_click:
        try:
            elt.click()
            logging.debug("Clicking on elt {}".format(elt.text))
        except ElementClickInterceptedException as err:
            logging.error("ElementClickInterceptedException: {}".format(err))

    time.sleep(2)
    remove_sign_up_prompt(driver)
    remove_recommended_jobs(driver)
    tabs_category = driver.find_element_by_class_name("scrollableTabs")
    tabs_category = tabs_category.find_elements_by_class_name("tab")
    get_data_from_tabs(driver, job, tabs_category)


def get_data_from_tabs(driver, job, tabs_category):
    """click on each tab to get the data and completes job with the received information"""
    for tab in tabs_category:
        try:
            tab.click()
        except ElementClickInterceptedException as err:
            logging.error("ElementClickInterceptedException: {}".format(err))
        time.sleep(.1)
        detail_tab = driver.find_element_by_class_name("jobDetailsInfoWrap")
        html_detail_tab = detail_tab.get_attribute('innerHTML')
        name_category = tab.text
        parse_tab(html_detail_tab, job, name_category)
        save_data_to_file(html_detail_tab, name_category)


def parse_tab(html_detail_tab, job, name_category):
    """Select the appropriate method from TabScrapping based on the name of the tab"""
    if name_category == 'Company':
        company_data_dict = scrape_company_tab(html_detail_tab)
        job.company.add_data_dict(company_data_dict)
    elif name_category == 'Rating':
        job.company['rating'] = rating(html_detail_tab)
        job.company['rating_count'] = nbr_of_ratings(html_detail_tab)
    elif name_category == 'Benefits':
        job.company['benefits_rating'] = benefits_rate(html_detail_tab)
        job.company['benefits_rating_count'] = nbr_of_benefits_rating(html_detail_tab)


def save_data_to_file(html_detail_tab, name_category):
    """saves us a copy of the html that was parsed"""
    name_saved_data = name_category + ".html"
    with open(name_saved_data, 'a+') as f:
        f.write(html_detail_tab)


def create_output_folder():
    """create output folder with saved data"""
    if not os.path.lexists(SAVED_DATA):
        os.mkdir(SAVED_DATA)
    os.chdir(SAVED_DATA)
    data_dir_by_date = datetime.datetime.now().strftime("data-%d-%b_%H:%M:%S")
    os.mkdir(data_dir_by_date)
    os.chdir(data_dir_by_date)


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
    """Will launch each data """
    list_job_offers = driver.find_elements_by_class_name("jobContainer")
    jobs = []
    for i, elt in enumerate(list_job_offers):
        should_click = True
        if i == 0:
            should_click = False  # We don't need to should_click on the first link since we are already seeing it
        remove_sign_up_prompt(driver)
        remove_recommended_jobs(driver)
        html_job_container = elt.get_attribute('innerHTML')
        time.sleep(2)
        name_company = get_name_company(elt.text)
        company = Company(name_company)
        job_id = get_job_id(html_job_container)
        job = JobOffer(job_id, company=company)
        company_and_id_job = name_company + "-" + job_id
        os.mkdir(company_and_id_job)
        os.chdir(company_and_id_job)
        scrape_data_company(driver, elt, job, should_click)
        os.chdir("..")
        jobs.append(job)
        print(job)
    print_jobs(jobs)


def init_job_page(base_url, driver):
    driver.get(base_url)
    driver.implicitly_wait(100)


def remove_sign_up_prompt(driver):
    """Method to remove sign up prompt so we won't have to login"""
    try:
        driver.find_element_by_class_name("selected").click()
    except ElementClickInterceptedException:
        pass

    driver.implicitly_wait(.1)

    try:
        driver.find_element_by_class_name("ModalStyle__xBtn___29PT9").click()  # clicking the X
    except NoSuchElementException:
        pass


def remove_recommended_jobs(driver):
    """Sometimes it appears """
    try:
        driver.find_element_by_class_name("selected").click()
    except ElementClickInterceptedException:
        pass

    driver.implicitly_wait(.1)

    try:
        driver.find_element_by_class_name("secondaryCTAButton").click()  # clicking the X
    except NoSuchElementException:
        pass
    except ElementNotInteractableException:
        pass


def get_geckodriver():
    """We have included the geckodriver for firefox for windows mac and linux"""
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


if __name__ == '__main__':
    main()
