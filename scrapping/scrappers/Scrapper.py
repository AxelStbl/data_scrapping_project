import datetime
import time
import os
import re
import urllib.parse

from selenium.common.exceptions import StaleElementReferenceException, \
    NoSuchElementException, ElementClickInterceptedException, \
    ElementNotInteractableException
from bs4 import BeautifulSoup
import json
import requests
import scrapping.conf.properties as conf
import scrapping.data_classes.Company as Company
import scrapping.data_classes.JobOffer as JobOffer
import scrapping.scrappers.TabScrapping as TabScrapping

logger = conf.configure_logger()


class Scrapper:
    def __init__(self, driver, path_to_save, db_connection):
        """
        Initiate the scrapper
        :param db_connection: the db we want to connect to
        :param driver: the selenium driver
        """
        self.db_connection = db_connection
        self.driver = driver
        self.date_path = path_to_save
        self.current_path = path_to_save

    def scrape_data_company(self, elt, company):
        """Will click on the company name and each category so we
        can then store data
        :param elt: company job offer link
        :param company: """

        try:
            self.wait_job_loading(elt)
            self.remove_sign_up_prompt()
            self.remove_recommended_jobs()
            tabs_category = self.driver.find_element_by_class_name(
                "scrollableTabs")
            tabs_category = tabs_category.find_elements_by_class_name("tab")
            self.get_data_from_tabs(company, tabs_category)

        except TimeoutError:
            logger.error("Timeout was reached and data was not loaded")
        except StaleElementReferenceException as err:
            logger.error("Trying to click on a stale element ", err)

    def wait_job_loading(self, elt, timeout=10):
        """
        Wait for the job offer to be loaded onto screen
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
                employer_info_txt = self.driver.find_element_by_class_name(
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

    def get_data_from_tabs(self, company, tabs_category):
        """click on each tab to get the data and completes job with
        the received information
        :param company: company instance
        :param tabs_category: different tabs that we could click on
        """
        for tab in tabs_category:
            try:
                tab.click()
            except ElementClickInterceptedException as err:
                logger.error(
                    "ElementClickInterceptedException: {}".format(err))
            time.sleep(.1)
            detail_tab = self.driver.find_element_by_class_name(
                "jobDetailsInfoWrap")
            html_detail_tab = detail_tab.get_attribute('innerHTML')
            name_category = tab.text
            tab_scrapper = TabScrapping.TabScrapping(html_detail_tab)
            tab_scrapper.parse_tab(company, name_category)
            if conf.SAVE_HTML_TO_FILE:
                self.save_data_to_file(html_detail_tab, name_category)

    def scrap_data_companies(self):
        """Will scrape and then print each data collected
        """
        list_job_offers = self.driver.find_elements_by_class_name(
            "jobContainer")
        jobs = []
        if len(list_job_offers) == 0:
            print("There is nothing  to scrap for ", conf.URL_TO_SCRAPE,
                  "that was requested")
            return

        for i, elt in enumerate(list_job_offers):

            self.remove_sign_up_prompt()
            self.remove_recommended_jobs()
            html_job_container = elt.get_attribute('innerHTML')
            time.sleep(2)
            name_company = get_name_company(elt.text)
            city_job = get_city_job(html_job_container)
            job_id = get_job_id(html_job_container)
            position_job = get_position(html_job_container)
            job_description = get_summary_job(position_job)

            if job_id is not None and name_company is not None:
                company = Company.Company(name_company)
                company_and_id_job = name_company + "-" + job_id
                self.current_path = os.path.join(self.date_path,
                                                 company_and_id_job)
                os.mkdir(self.current_path)

                if i != 0:
                    click_on_job_offer(
                        elt)  # link since we are already seeing it

                self.scrape_data_company(elt, company)
                company_id = company.insert_to_db(self.db_connection)
                job = JobOffer.JobOffer(job_id, company=company, city=city_job,
                                        position=position_job,
                                        description=job_description)
                job.insert_to_db(company_id, self.db_connection)
                jobs.append(job)
                print(job)
            else:
                logger.error("Job Id not found")
        JobOffer.print_jobs(jobs)

    def init_job_page(self, base_url):
        """
        Call the requested url with the provided driver and wait  100 sec
        :param base_url: url you want to open
        """
        self.driver.get(base_url)
        self.driver.implicitly_wait(100)

    def remove_sign_up_prompt(self):
        """Method to remove sign up prompt so we won't have to login
        """
        is_modal_present = self.detect_obscuring_windows()
        self.driver.implicitly_wait(.1)
        if is_modal_present:
            self.close_sign_up_prompt()

    def close_sign_up_prompt(self):
        """Close sign up prompt if present
        """
        try:
            self.driver.find_element_by_class_name('modal_closeIcon').click()
        except NoSuchElementException:
            logger.info("No Element Found to Close")

    def detect_obscuring_windows(self):
        """Detect if a windows like the sign up prompt is present
        :return: True if element is hiding the view else False
        """
        try:
            self.driver.find_element_by_class_name("selected").click()
        except ElementClickInterceptedException:
            logger.info("Detecting element obscuring the window")
            return True
        return False

    def remove_recommended_jobs(self):
        """Sometimes it appears a small recommended job modal
        that we can make disappear
        """
        if self.detect_obscuring_windows():
            self.driver.implicitly_wait(.1)
            try:
                self.driver.find_element_by_class_name(
                    "secondaryCTAButton").click()  # clicking the X
            except NoSuchElementException as err:
                logger.debug("Recommanded jobs modal not present ", err)
            except ElementNotInteractableException as err:
                logger.debug(
                    "The obscuring element is probably",
                    "not the recommended modal ",
                    err)

    def create_output_folder(self):
        """create output folder with html saved data
        :return: the relative path of the created folder by date
        """
        if not os.path.exists(self.current_path):
            os.mkdir(self.current_path)
        data_dir_by_date = datetime.datetime.now().strftime(
            "data-%d-%b_%H-%M-%S")
        self.date_path = os.path.join(self.current_path, data_dir_by_date)
        if not os.path.exists(self.date_path):
            os.mkdir(self.date_path)

    def save_data_to_file(self, html_detail_tab, name_category):
        """saves us a copy of the html that was parsed
        :param html_detail_tab: html detail tab that was provided
        :param name_category: name category to save
        """
        name_saved_data = name_category + ".html"
        with open(os.path.join(self.current_path, name_saved_data), 'a+') as f:
            try:
                f.write(html_detail_tab)
            except IOError as io:
                logger.error(
                    "caught an io exception while writing to the file",
                    io)


def get_name_company(html_job_container):
    """find the job name from html
    :param html_job_container:
    :return: the name of the company
    """
    lines = html_job_container.splitlines()
    if len(lines) > 0:
        return lines[0]
    return None


def get_position(html_job_container):
    """
    Return job position title
    :param html_job_container: data to scrape
    :return: job title
    """
    soup = BeautifulSoup(html_job_container, 'html.parser')
    job_position = soup.find_all(
        class_="jobLink jobInfoItem jobTitle")  # .get_text()
    if len(job_position) == 2:
        return job_position[1].get_text()
    return None


def get_city_job(html):
    """
    Return the city where the job is located
    :param html:
    :return: city
    """
    soup = BeautifulSoup(html, 'html.parser')
    city = soup.find(class_="subtle loc").get_text()
    if city:
        return city
    return None


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


def get_job_id(html_job_container):
    """find the id of the job from the html container
    :param html_job_container:
    :return: the id of the job or None if not found
    """
    match = re.search(r'jobListingId=(\d*)"', html_job_container)
    if match:
        return match.group(1)
    return None


def get_summary_job(job):
    """
    Get a short summary about the specified position
    :param job: the job we want to have the description
    :return: a short extract from Wikipedia if found else None
    """
    if job is None:
        return None
    url = conf.WIKIPEDIA_URL.format(
        urllib.parse.quote(job))

    r = requests.get(url).content
    data_loaded = json.loads(r)
    if type(data_loaded) == dict and data_loaded['title'] != 'Not found.':
        summary = data_loaded['extract']
        if len(summary) < 65535:
            return summary
        else:
            logger.info('Summary for job is too long to fit into the table',
                        job)
            return None
    else:
        logger.info('Description not found for the following job', job)
        return None
