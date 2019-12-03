import re
from bs4 import BeautifulSoup

import scrapping.conf.properties as conf


class TabScrapping:
    def __init__(self, data_to_scrape):
        self.data_to_scrape = data_to_scrape

    def scrape_company_tab(self):
        """scrape data about companies
        :return: dictionary containing various info about the company
        """
        soup = BeautifulSoup(self.data_to_scrape, 'html.parser')
        company_data = soup.find_all('div', class_="infoEntity")
        label_value_data = {}
        if len(company_data) > 0:
            for info in company_data:
                label_value_data[info.label.getText().lower()] = \
                    info.find('span', class_='value').get_text()

            span_website = soup.find('span', class_="website")
            if span_website:
                website_link = span_website.find('a', href=True)
                label_value_data["website"] = website_link['href']
        return label_value_data

    def rating(self):
        """Find the rating of the company
        :return: return the rating out of 5 star
        """
        soup = BeautifulSoup(self.data_to_scrape, 'html.parser')
        rate = soup.find(class_="ratingNum margRtSm").get_text()
        if not rate:
            return None
        return rate

    def nbr_of_ratings(self):
        """Returns the number of the person who rated
        :return: return total amount of ratings
        """
        soup = BeautifulSoup(self.data_to_scrape, 'html.parser')
        allnbr = str(soup.find(class_="ct-bar"))
        if not allnbr:
            return None
        rating_counts = []
        values = soup.find_all('line', class_="ct-bar")
        if not values:
            return None
        for value in values:
            match = re.search(r'value="(\d*)"', str(value))
            if not match:
                return None
            nbr = int((match).group(1))
            rating_counts.append(nbr)
        sum = 0
        for rating in rating_counts:
            sum += rating
        return sum

    def benefits_rate(self):
        """ scrape the benefits rate of the company
        :return: the rating of the benefits of the company
        """
        soup = BeautifulSoup(self.data_to_scrape, 'html.parser')
        rate = soup.find(class_="ratingNum margRtSm").get_text()
        if not rate:
            return None
        return rate

    def salary(self):
        """ WORK IN PROGRESS
                To scrape the average salaries for each job title
                :return: a mean of all the job title were appears the name of the job we search for.
                """
        soup = BeautifulSoup(self.data_to_scrape, 'html.parser')
        data_salary = soup.find_all(class_="noMarg salaryRow row")
        list_salary = []
        sum = 0
        for line in data_salary:
            average_salary = line.get_text().split('$')[4]
            job_title = line.get_text().split('$')[0]
            if conf.JOB in job_title:
                average_salary = int(average_salary.replace(',', ''))
                list_salary.append(average_salary)
                sum += average_salary
        if len(list_salary) == 0:
            return None
        mean = sum / len(list_salary)
        return int(mean)

    def nbr_of_benefits_rating(self):
        """Returns the nbr of benefits a company received
        :return:  the number of ppl who rated for the benefits of the company
        or None if not found
        """
        soup = BeautifulSoup(self.data_to_scrape, 'html.parser')
        nbr_of_ratings = soup.find(class_="minor noMargTop padSm").get_text()
        if nbr_of_ratings:
            matches = re.findall(r'\d', nbr_of_ratings)
            if len(matches) == 1:
                return matches[0]
        return None

    def parse_tab(self, company, name_category):
        """Select the appropriate method from TabScrapping based on the name of
        the tab
        :param company: company instance
        :param name_category: name of the tab
        """
        if name_category == 'Company':
            company_data_dict = self.scrape_company_tab()
            company.add_data_dict(company_data_dict)
        elif name_category == 'Rating':
            company['rating'] = self.rating()
            company['rating_count'] = self.nbr_of_ratings()
        elif name_category == 'Benefits':
            company['benefits_rating'] = self.benefits_rate()
            company['benefits_rating_count'] = self.nbr_of_benefits_rating()
