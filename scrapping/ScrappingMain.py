import scrapping.scrappers.Scrapper as sc
import scrapping.conf.properties as conf

logger = conf.configure_logger()


def main():
    """Main function launch our functions"""

    # Firefox session
    # Chooses the right executable
    driver = conf.get_geckodriver()
    if not driver:
        print("Driver not found for your operating system")
        return
    scrapper = sc.Scrapper(driver, conf.SAVED_DATA)
    conf.date_path = scrapper.create_output_folder()
    scrapper.init_job_page(conf.BASE_URL)
    scrapper.scrap_data_companies()

    if conf.QUIT:  # not quitting for debugging purposes
        driver.quit()


if __name__ == '__main__':
    main()
