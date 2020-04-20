import os
import random
import sys
import time

with open("list_of_jobs_to_scrape.txt", 'r') as f:
    jobs = f.read()
jobs = jobs.splitlines()
for job in jobs:
    sys.argv = ['o', '--job', job, '--no_recap',
                '--no_save_html']
    try:
        p = os.popen(
            'python -m scrapping --job --headless "{}" --no_save_html'.format(
                job))
        print(p.read())
        # scrapping.ScrappingMain.main()
    except:
        time.sleep(random.randint(100, 200))
    # break
