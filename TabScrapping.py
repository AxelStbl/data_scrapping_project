import re
from bs4 import BeautifulSoup


def rating(data):
    """Returns the rating of the company"""
    soup = BeautifulSoup(data)
    rate = soup.find(class_="ratingNum margRtSm").get_text()
    return rate


def nbr_of_ratings(data):
    """Returns the number of the person who rated"""
    soup = BeautifulSoup(data)
    allnbr = str(soup.find(class_="ct-bar"))
    nbr = int(re.search(r'value="(\d*)"', allnbr).group(1))
    nbr_of_ratings = []
    values = soup.find_all('line', class_="ct-bar")
    for value in values:
        nbr = int(re.search(r'value="(\d*)"', str(value)).group(1))
        nbr_of_ratings.append(nbr)
    sum = 0
    for nbr in nbr_of_ratings:
        sum += nbr
    return sum


def benefits_rate(data):
    """Returns the rating of the benefits of the company"""
    soup = BeautifulSoup(data)
    rate = soup.find(class_="ratingNum margRtSm").get_text()
    return rate


def nbr_of_benefitsrating(data):
    """Returns the number of ppl who rated for the benefits of the company
    """
    soup = BeautifulSoup(data)
    nbr_of_ratings = soup.find(class_="minor noMargTop padSm").get_text()
    return nbr_of_ratings


# def main():
#     fd_rating = open('Rating.html','r')
#     data_rating = fd_rating.read()
#     fd_rating.close()
#     fd_benefits = open('Benefits.html','r')
#     data_benefits = fd_benefits.read()
#     fd_benefits.close()
#     print(rating(data_rating))
#     print(nbr_of_ratings(data_rating))
#     print(benefits_rate(data_benefits))
#     print(nbr_of_benefitsrating(data_benefits))

#if __name__ == '__main__':
#    main()