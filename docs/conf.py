# All config here that can be tuned
# importing module
import logging

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
    logger.setLevel(logging.DEBUG)
    return logger
