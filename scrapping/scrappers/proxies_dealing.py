'''
import logging
import random
import requests
from bs4 import BeautifulSoup
import fake_useragent
from fake_useragent import UserAgent, FakeUserAgentError
from itertools import cycle

import scrapping.conf.properties


class utilities_proxies:
    def proxies_pool(self):
        url = 'https://www.sslproxies.org/'

        # Retrieve the site's page. The 'with'(Python closure) is used here in order to automatically close the session when done
        with requests.Session() as res:
            proxies_page = res.get(url)

        # Create a BeutifulSoup object and find the table element which consists of all proxies
        soup = BeautifulSoup(proxies_page.content, 'html.parser')
        proxies_table = soup.find(id='proxylisttable')

        # Go through all rows in the proxies table and store them in the right format (IP:port) in our proxies list
        proxies = []
        for row in proxies_table.tbody.find_all('tr'):
            proxies.append('{}:{}'.format(row.find_all('td')[0].string,
                                          row.find_all('td')[1].string))
        return proxies

    def random_header(self, logger=None):
        if logger is None:
            logger = logging
        # Create a dict of accept headers for each user-agent.
        accepts = {
            "Firefox": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Safari, Chrome": "application/xml,application/xhtml+xml,text/html;q=0.9, text/plain;q=0.8,image/png,*/*;q=0.5"}

        # Get a random user-agent. We used Chrome and Firefox user agents.
        # Take a look at fake-useragent project's page to see all other options - https://pypi.org/project/fake-useragent/
        try:
            # Getting a user agent using the fake_useragent package
            ua = UserAgent()
            if random.random() > 0.5:
                random_user_agent = ua.chrome
            else:
                random_user_agent = ua.firefox

        # In case there's a problem with fake-useragent package, we still want the scraper to function
        # so there's a list of user-agents that we created and swap to another user agent.
        # Be aware of the fact that this list should be updated from time to time.
        # List of user agents can be found here - https://developers.whatismybrowser.com/.
        except FakeUserAgentError  as error:
            # Save a message into a logs file. See more details below in the post.
            logger.error(
                "FakeUserAgent didn't work. Generating headers from the pre-defined set of headers. error: {}".format(
                    error))
            user_agents = [
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36",
                "Mozilla/5.0 (Windows NT 5.1; rv:7.0.1) Gecko/20100101 Firefox/7.0.1"]  # Just for case user agents are not extracted from fake-useragent package
            random_user_agent = random.choice(user_agents)

        # Create the headers dict. It's important to match between the user-agent and the accept headers as seen in line 35
        finally:
            valid_accept = accepts['Firefox'] if random_user_agent.find(
                'Firefox') > 0 else accepts['Safari, Chrome']
            headers = {"User-Agent": random_user_agent,
                       "Accept": valid_accept}
        return headers

    # Generate the pools
    def create_pools(self):
        proxies = self.proxies_pool()
        headers = [
            self.random_header(None)
            for ind in
            range(
                len(
                    proxies))]  # list of headers, same length as the proxies list

        # This transforms the list into itertools.cycle object (an iterator) that we can run
        # through using the next() function in lines 16-17.
        proxies_pool = cycle(proxies)
        headers_pool = cycle(headers)
        return proxies_pool, headers_pool


# Usage example
test = utilities_proxies()
proxies_pool, headers_pool = test.create_pools()
current_proxy = next(proxies_pool)
current_headers = next(headers_pool)

# Introduce the proxy and headers in the GET request
# with requests.Session() as req:
#   page = req.get("https://www.google.com",
#                 proxies={"http": current_proxy, "https": current_proxy},
#                headers=current_headers, timeout=30)
# print(page.text)
#print(test.proxies_pool())
# print(test.random_header(prop.configure_logger()))


current_proxy = "52.74.155.41:8080"
# proxy = Proxy({
#     'proxyType': ProxyType.MANUAL,
#     'httpProxy': myProxy,
#     'ftpProxy': myProxy,
#     'sslProxy': myProxy,
#     'noProxy': ''  # set this value as desired
# })
# #options.proxy = myProxy
# driver = webdriver.Firefox(executable_path=executable_path,
#                            proxy=proxy)
# driver.get("http://www.whatismyproxy.com/")
test = utilities_proxies()
proxies_pool, headers_pool = test.create_pools()
# current_proxy = next(proxies_pool)


current_headers = next(headers_pool)
print(current_proxy)
firefox_capabilities = webdriver.DesiredCapabilities.FIREFOX
firefox_capabilities['marionette'] = True

firefox_capabilities['proxy'] = {
    "proxyType": "MANUAL",
    "httpProxy": current_proxy,
    "ftpProxy": current_proxy,
    "sslProxy": current_proxy
}
# print(firefox_capabilities)
profile = webdriver.FirefoxProfile()
# profile.set_preference("general.useragent.override",
#                        str(current_headers))
driver = webdriver.Firefox(executable_path=executable_path,
                           options=options)
'''
