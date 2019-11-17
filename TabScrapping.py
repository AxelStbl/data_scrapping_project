import re
from bs4 import BeautifulSoup
import os


def scrape_company_tab(data):
    """scrape data about companies"""
    soup = BeautifulSoup(data, 'html.parser')
    company_data = soup.find_all('div', class_="infoEntity")
    if not company_data:
        return None
    label_value_data = {}
    if len(company_data) > 0:
        for data in company_data:
            label_value_data[data.label.getText().lower()] = data.find('span', class_='value').get_text()

        span_website = soup.find('span', class_="website")
        if not span_website:
            return None
        if span_website:
            website_link = span_website.find('a', href=True)
            label_value_data["website"] = website_link['href']
    return label_value_data


def rating(data):
    """Returns the rating of the company"""
    soup = BeautifulSoup(data, 'html.parser')
    rate = soup.find(class_="ratingNum margRtSm").get_text()
    if not rate:
        return None
    return rate


def nbr_of_ratings(data):
    """Returns the number of the person who rated"""
    soup = BeautifulSoup(data, 'html.parser')
    allnbr = str(soup.find(class_="ct-bar"))
    if not allnbr:
        return None
    nbr_of_ratings = []
    values = soup.find_all('line', class_="ct-bar")
    if not values:
        return None
    for value in values:
        match = re.search(r'value="(\d*)"', str(value))
        if not match:
            return None
        nbr = int((match).group(1))
        nbr_of_ratings.append(nbr)
    sum = 0
    for nbr in nbr_of_ratings:
        sum += nbr
    return sum

def benefits_rate(data):
    """Returns the rating of the benefits of the company"""
    soup = BeautifulSoup(data, 'html.parser')
    rate = soup.find(class_="ratingNum margRtSm").get_text()
    if not rate:
        return None
    return rate


def nbr_of_benefitsrating(data):
    """Returns the number of ppl who rated for the benefits of the company
    """
    soup = BeautifulSoup(data, 'html.parser')
    nbr_of_ratings = soup.find(class_="minor noMargTop padSm").get_text()
    if not nbr_of_ratings:
        return None
    return nbr_of_ratings


def main():
    if not os.path.exists('Rating.html'):
        return
    if not os.path.exists('Benefits.html'):
        return
    if not os.path.exists('Company.html'):
        return
    fd_rating = open('Rating.html', 'r')
    data_rating = fd_rating.read()
    fd_rating.close()
    fd_benefits = open('Benefits.html', 'r')
    data_benefits = fd_benefits.read()
    fd_benefits.close()
    print(rating(data_rating))
    print(nbr_of_ratings(data_rating))
    print(benefits_rate(data_benefits))
    print(nbr_of_benefitsrating(data_benefits))
    fd_comp = open('Company.html', 'r')
    data_cmp = fd_comp.read()
    fd_comp.close()
    print(scrape_company_tab(data_cmp))


if __name__ == '__main__':
    main()
