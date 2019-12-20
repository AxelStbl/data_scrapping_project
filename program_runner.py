import scrapping.ScrappingMain
import sys
import random
import time

with open("list_of_jobs_to_scrape.txt", 'r') as f:
    jobs = f.read()
jobs = jobs.splitlines()
for job in jobs:
    sys.argv = ['o', '-headless', '-job', job, '-no_recap',
                '-no_save_html']
    try:
        scrapping.ScrappingMain.main()
    except:
        time.sleep(random.randint(100, 200))
