import re
from bs4 import BeautifulSoup


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

    def nbr_of_benefits_rating(self):
        """Returns the nbr of benefits a company received
        :return:  the number of ppl who rated for the benefits of the company
        """
        soup = BeautifulSoup(self.data_to_scrape, 'html.parser')
        nbr_of_ratings = soup.find(class_="minor noMargTop padSm").get_text()
        if not nbr_of_ratings:
            return None
        return nbr_of_ratings
