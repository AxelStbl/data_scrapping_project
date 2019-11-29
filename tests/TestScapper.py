import os

from scrapping import *


def test_scrapper():
    """Use our scrapper on data for test"""
    rating_path = 'test_data/Rating.html'
    if not os.path.exists(rating_path):
        return
    benefits_path = 'test_data/Benefits.html'
    if not os.path.exists(benefits_path):
        return
    company_path = 'test_data/Company.html'
    if not os.path.exists(company_path):
        return
    fd_rating = open(rating_path, 'r')
    data_rating = fd_rating.read()
    fd_rating.close()
    fd_benefits = open(benefits_path, 'r')
    data_benefits = fd_benefits.read()
    fd_benefits.close()
    print(rating(data_rating))
    print(nbr_of_ratings(data_rating))
    print(benefits_rate(data_benefits))
    print(nbr_of_benefits_rating(data_benefits))
    fd_comp = open(company_path, 'r')
    data_cmp = fd_comp.read()
    fd_comp.close()
    print(scrape_company_tab(data_cmp))


if __name__ == '__main__':
    test_scrapper()
