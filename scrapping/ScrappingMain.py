import argparse

import scrapping.conf.properties as conf
import scrapping.scrappers.Scrapper as sc
import urllib.parse

logger = conf.configure_logger()


def main():
    """Main function launch our functions"""
    arg_parser()

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


def arg_parser():
    parser = argparse.ArgumentParser(
        description='To give parameters of configurations for the project')

    parser.add_argument("-headless",
                        help="To see the firefox headless, by default : False",
                        action='store_true')
    parser.add_argument("-quit",
                        help="To quit the program, by default : True "
                             "(For debugging purpose)",
                        action='store_false')
    parser.add_argument("-saved_data", default=conf.SAVED_DATA,
                        help="Name of the folder to save the data",
                        type=str)
    parser.add_argument("-recap",
                        help="to get a resume of all the data who were print "
                             "one by one, by default True",
                        action='store_false')
    parser.add_argument("-job", help="Name of the job you want to scrap",
                        default=conf.JOB, dest='job',
                        type=str)
    args = parser.parse_args()

    conf.HEADLESS = args.headless
    conf.QUIT = args.quit
    conf.RECAP = args.recap
    conf.JOB = urllib.parse.quote(args.job)
    conf.BASE_URL = conf.url_job()
    conf.SAVED_DATA = args.saved_data
    print("Launching with the following parameters enter -h for more infos"
          " about them: HEADLESS {} , JOB: {}, QUIT: {} , RECAP: {},"
          " NAME DATA FOLDER: {} ".format(
        conf.HEADLESS, urllib.parse.unquote(conf.JOB), conf.QUIT, conf.RECAP,
        conf.SAVED_DATA))

    if __name__ == '__main__':
        main()
