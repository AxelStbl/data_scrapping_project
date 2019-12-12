import scrapping.conf.connector_db as conn
import json
import requests


ATTRIBUTES_TO_STRING = dict(name="Name",
                            headquarters_city="Headquarters localisation (city)",
                            headquarters_country="Headquarters localisation (country)",
                            headquarters_currency="Headquarters currency (currency)",
                            rating="Rating",
                            rating_count="Total ratings",
                            benefits_rating="Benefits Rating",
                            benefits_rating_count="Benefits Rating Total",
                            nb_of_employees="Size", founded="Year foundation",
                            type="Company Type", website="Website",
                            competitors="Competitors")


class Company:
    def __init__(self, name, headquarters_city=None, headquarters_country=None, headquarters_currency=None, rating=None, rating_count=None,
                 benefits_rating=None,
                 benefits_rating_count=None, nb_of_employees=None,
                 founded=None,
                 type=None, website=None, competitors=None):
        """
        init parameters
        :param name: name of the company
        :param headquarters_city: headquarters localization (city)
        :param headquarters_country: headquarters localization (country)
        :param headquarters_currency: headquarters localization (currency)
        :param rating: global rating out of 5 of the company
        :param rating_count: number of ratings
        :param benefits_rating: rating concerning the benefits out of 5
        :param benefits_rating_count: numbers of votes for benefits rating
        :param nb_of_employees: number of employees
        :param founded: date of creation of company
        :param type: type of the company
        :param website: website of the company
        :param competitors: existing competitors
        """
        self.name = name
        self.headquarters_city = headquarters_city
        self.headquarters_country = headquarters_country
        self.headquarters_currency = headquarters_currency
        self.rating = rating
        self.rating_count = rating_count
        self.benefits_rating = benefits_rating
        self.benefits_rating_count = benefits_rating_count
        self.nb_of_employees = nb_of_employees
        self.founded = founded
        self.type = type
        self.website = website
        self.competitors = competitors

    def add_data_dict(self, data_dict):
        """replace all values by their corresponding value
        :param data_dict: completes attributes of the company based on a key
        value dict
        """
        for key, value in data_dict.items():
            if key in vars(self):
                self[key] = value
            elif key == 'headquarters':
                self.headquarters_city = value.split(',')[0].strip()
                self.headquarters_country = value.split(',')[1].strip()
                self.headquarters_currency = get_currency(self.headquarters_country)

    def __setitem__(self, key, value):
        """
        precise how to set an item in this class
        :param key: key to set
        :param value: value to put
        """
        self.__setattr__(key, value)

    def insert_to_db(self):
        """
        Insert data from company object to the database
        :return: id of the company created or fetched
        """
        db = conn.get_db_conn()
        cur = db.cursor()
        id_company, company = self.find_company_by_id(cur)
        if company is not None:
            self.update_data_company(company, cur, db)
            return id_company
        cur.execute(
            "INSERT INTO companies (name, headquarters_city, headquarters_country, headquarters_currency, "
            "rating, rating_count,"
            "benefits_rating, benefits_rating_count, nb_of_employees,"
            " founded, type, website, competitors) "
            "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
            (self.name, self.headquarters_city,self.headquarters_country ,self.headquarters_currency, self.rating, self.rating_count,
             self.benefits_rating, self.benefits_rating_count,
             self.nb_of_employees,
             self.founded, self.type,
             self.website, self.competitors))
        db.commit()
        id_company, _ = self.find_company_by_id(cur)
        return id_company

    def update_data_company(self, company, cur, db):
        """
        will update field by field company if necessary
        :param company: company to update
        :param cur: sql current session
        :param db: database
        """
        for var in vars(self):
            if company.__getattribute__(var) is None and self.__getattribute__(
                    var) is not None:
                cur.execute(
                    "UPDATE companies SET {} = %s WHERE name=%s".format(
                        var),
                    (self.__getattribute__(var), self.name))
        db.commit()

    def find_company_by_id(self, cur):
        """
        execute request to find the id of the company
        :param cur: name of the company
        :return: id of the company
        """
        cur.execute("SELECT * FROM companies where name = %s", (self.name,))
        exist = cur.fetchall()
        if len(exist) == 1:
            return exist[0][0], Company(
                *exist[0][1:])  # because first element is id
        return None, None

    def __repr__(self):
        """
        Creates string representation of the object
        :return: string of the company data aggregation
        """
        res = "Company: \n"
        for var in vars(self):
            if self.__getattribute__(var):
                res += "\t" + ATTRIBUTES_TO_STRING[var] + ": " + str(
                    self.__getattribute__(var)) + "\n"
        return res


def main():
    c1 = Company("Facebook", headquarters_city="Palo alto", benefits_rating=3.4,
                 benefits_rating_count=120,
                 founded=2004, type="Software",
                 website="https://www.facebook.com", rating=4,
                 rating_count=124)
    print(c1)



def get_currency(country):
    """Take the currency data of the country of the company on the API of the website restcountries.eu
    :param country: country to get currency
    :return: the name of the currency
    """
    #TODO handle exceptions and not working
    URL = 'https://restcountries.eu/rest/v2/name/{}?fullText=true'.format(country)
    r = requests.get(URL).content
    data = json.loads(r)[0]
    name_cur = data['currencies'][0]['name']
    return name_cur

if __name__ == '__main__':
    main()
