import datetime
import platform
import time

from selenium import webdriver
from selenium.common.exceptions import ElementClickInterceptedException, \
    NoSuchElementException, \
    ElementNotInteractableException, StaleElementReferenceException
from selenium.webdriver.firefox.options import Options

import docs.conf as conf
from scrapping import *

logger = conf.configure_logger()


def scrape_data_company(driver, elt, job):
    """Will click on the company name and each category so we can then store
    data
    :param driver: Selenium driver
    :param elt: company job offer link
    :param job: """

    try:
        wait_job_loading(driver, elt)
        remove_sign_up_prompt(driver)
        remove_recommended_jobs(driver)
        tabs_category = driver.find_element_by_class_name("scrollableTabs")
        tabs_category = tabs_category.find_elements_by_class_name("tab")
        get_data_from_tabs(driver, job, tabs_category)
    except TimeoutError:
        logger.error("Timeout was reached and data was not loaded")
    except StaleElementReferenceException as err:
        logger.error("Trying to click on a stale element ", err)


def wait_job_loading(driver, elt, timeout=10):
    """
    Wait for the job offer to be loaded onto screen
    :param driver: selenium driver
    :param elt: the job offer link
    :param timeout: can customize the max duration of the waiting
    """
    time_slept = 0
    wait = True
    while wait:
        time.sleep(1)
        time_slept += 1
        company_name = elt.text.splitlines()[0]
        try:
            employer_info_txt = driver.find_element_by_class_name(
                "empInfo").text.splitlines()[0]
            if (employer_info_txt.splitlines()[0]
                    == company_name):
                wait = False
        except NoSuchElementException as err:
            logger.error("Element not found ", err)
        if time_slept > timeout:
            raise TimeoutError(
                "job offer of {} was not loaded in 10 seconds".format(
                    company_name))


def get_data_from_tabs(driver, job, tabs_category):
    """click on each tab to get the data and completes job with the received
    information
    :param driver: selenium driver
    :param job: job instance
    :param tabs_category: different tabs that we could click on
    """
    for tab in tabs_category:
        try:
            tab.click()
        except ElementClickInterceptedException as err:
            logger.error(
                "ElementClickInterceptedException: {}".format(err))
        time.sleep(.1)
        detail_tab = driver.find_element_by_class_name("jobDetailsInfoWrap")
        html_detail_tab = detail_tab.get_attribute('innerHTML')
        name_category = tab.text
        parse_tab(html_detail_tab, job, name_category)
        save_data_to_file(html_detail_tab, name_category)


def parse_tab(html_detail_tab, job, name_category):
    """Select the appropriate method from TabScrapping based on the name of
    the tab
    :param html_detail_tab: html content of tab
    :param job: job instance
    :param name_category: name of the tab
    """
    scrapper = TabScrapping(html_detail_tab)
    if name_category == 'Company':
        company_data_dict = scrapper.scrape_company_tab()
        job.company.add_data_dict(company_data_dict)
    elif name_category == 'Rating':
        job.company['rating'] = scrapper.rating()
        job.company['rating_count'] = scrapper.nbr_of_ratings()
    elif name_category == 'Benefits':
        job.company['benefits_rating'] = scrapper.benefits_rate()
        job.company['benefits_rating_count'] = scrapper.nbr_of_benefits_rating(
        )


def save_data_to_file(html_detail_tab, name_category):
    """saves us a copy of the html that was parsed
    :param html_detail_tab: html detail tab that was provided
    :param name_category: name category to save
    """
    name_saved_data = name_category + ".html"
    with open(os.path.join(conf.current_path, name_saved_data), 'a+') as f:
        try:
            f.write(html_detail_tab)
        except IOError as io:
            logger.error(
                "caught an io exception while writing to the file",
                io)


def create_output_folder():
    """create output folder with html saved data
    :return: the relative path of the created folder by date
    """
    if not os.path.exists(conf.SAVED_DATA):
        os.mkdir(conf.SAVED_DATA)
    data_dir_by_date = datetime.datetime.now().strftime("data-%d-%b_%H:%M:%S")
    full_path_saved_data = os.path.join(conf.SAVED_DATA, data_dir_by_date)
    if not os.path.exists(full_path_saved_data):
        os.mkdir(full_path_saved_data)
    return full_path_saved_data


def get_job_id(html_job_container):
    """find the id of the job from the html container
    :param html_job_container:
    :return: the id of the job or None if not found
    """
    match = re.search(r'data-job-id="(\d*)"', html_job_container)
    if match:
        return match.group(1)
    return None


def get_name_company(html_job_container):
    """find the job name from html
    :param html_job_container:
    :return:
    """
    lines = html_job_container.splitlines()
    if len(lines) > 0:
        return lines[0]
    return None


def scrap_data_companies(driver):
    """Will launch each data
    :param driver: selenium driver
    """
    list_job_offers = driver.find_elements_by_class_name("jobContainer")
    jobs = []
    for i, elt in enumerate(list_job_offers):

        remove_sign_up_prompt(driver)
        remove_recommended_jobs(driver)
        html_job_container = elt.get_attribute('innerHTML')
        time.sleep(2)
        name_company = get_name_company(elt.text)
        job_id = get_job_id(html_job_container)

        if job_id is not None and name_company is not None:
            company = Company(name_company)
            job = JobOffer(job_id, company=company)
            company_and_id_job = name_company + "-" + job_id
            conf.current_path = os.path.join(conf.date_path,
                                             company_and_id_job)
            os.mkdir(conf.current_path)

            if i != 0:
                click_on_job_offer(elt)  # link since we are already seeing it

            scrape_data_company(driver, elt, job)
            jobs.append(job)
            print(job)
        else:
            logger.error("Job Id not found")
    print_jobs(jobs)


def click_on_job_offer(elt):
    """
    Simply in charge of clicking on the job offer
    :param elt: the link of the job offer
    """
    try:
        elt.click()
        logger.debug("Clicking on elt {}".format(elt.text))
    except ElementClickInterceptedException as err:
        logger.error("ElementClickInterceptedException: {}".format(err))


def init_job_page(base_url, driver):
    """
    Call the requested url with the provided driver and wait  100 sec
    :param base_url: url you want to open
    :param driver: selenium driver
    """
    driver.get(base_url)
    driver.implicitly_wait(100)


def remove_sign_up_prompt(driver):
    """Method to remove sign up prompt so we won't have to login
    :param driver: selenium driver
    """
    is_modal_present = detect_obscuring_windows(driver)
    driver.implicitly_wait(.1)
    if is_modal_present:
        close_sign_up_prompt(driver)


def close_sign_up_prompt(driver):
    """Close sign up prompt if present
    :param driver: selenium driver
    """
    try:
        driver.find_element_by_class_name('modal_closeIcon').click()
    except NoSuchElementException:
        logger.info("No Element Found to Close")


def detect_obscuring_windows(driver):
    """Detect if a windows like the sign up prompt is present
    :param driver: selenium driver
    :return: True if element is hiding the view else False
    """
    try:
        driver.find_element_by_class_name("selected").click()
    except ElementClickInterceptedException:
        logger.info("Detecting element obscuring the window")
        return True
    return False


def remove_recommended_jobs(driver):
    """Sometimes it appears a small recommended job modal that we can make
    disappear
    :param driver: selenium Webdriver
    """
    if detect_obscuring_windows(driver):
        driver.implicitly_wait(.1)
        try:
            driver.find_element_by_class_name(
                "secondaryCTAButton").click()  # clicking the X
        except NoSuchElementException as err:
            logger.debug("Recommanded jobs modal not present ", err)
        except ElementNotInteractableException as err:
            logger.debug(
                "The obscuring element is probably not the recommended modal ")


def get_geckodriver():
    """We have included the geckodriver for firefox for windows mac and
    linux
    :return: appropriate driver based on the os launching the app """
    running_system = platform.system()
    driver = None
    options = Options()
    options.headless = conf.HEADLESS
    executable_path = os.path.join("..", "drivers")
    if running_system == "Linux":
        executable_path = os.path.join(executable_path,
                                       "geckodriver-linux","geckodriver")
    elif running_system == "Darwin":
        executable_path = os.path.join(executable_path,
                                       "geckodriver-macos","geckodriver")
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


def main():
    """Main function launch our functions"""

    # Firefox session
    # Chooses the right executable
    driver = get_geckodriver()
    if not driver:
        print("Driver not found for your operating system")
        return
    conf.date_path = create_output_folder()
    init_job_page(conf.BASE_URL, driver)
    scrap_data_companies(driver)

    if conf.QUIT:  # not quitting for debugging purposes
        driver.quit()


if __name__ == '__main__':
    main()
