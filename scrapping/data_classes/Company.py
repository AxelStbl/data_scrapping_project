import scrapping.conf.connector_db as conn

ATTRIBUTES_TO_STRING = dict(name="Name",
                            headquarters="Headquarters localisation",
                            rating="Rating",
                            rating_count="Total ratings",
                            benefits_rating="Benefits Rating",
                            benefits_rating_count="Benefits Rating Total",
                            size="Size", founded="Year foundation",
                            type="Company Type", website="Website",
                            competitors="Competitors")


class Company:
    def __init__(self, name, headquarters=None, rating=None, rating_count=None,
                 benefits_rating=None,
                 benefits_rating_count=None, size=None, founded=None,
                 type=None, website=None, competitors=None):
        """
        init parameters
        :param name: name of the company
        :param headquarters: headquarters localization
        :param rating: global rating out of 5 of the company
        :param rating_count: number of ratings
        :param benefits_rating: rating concerning the benefits out of 5
        :param benefits_rating_count: numbers of votes for benefits rating
        :param size: number of employees
        :param founded: date of creation of company
        :param type: type of the company
        :param website: website of the company
        :param competitors: existing competitors
        """
        self.name = name
        self.headquarters = headquarters
        self.rating = rating
        self.rating_count = rating_count
        self.benefits_rating = benefits_rating
        self.benefits_rating_count = benefits_rating_count
        self.size = size
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

    def __setitem__(self, key, value):
        """
        precise how to set an item in this class
        :param key: key to set
        :param value: value to put
        """
        self.__setattr__(key, value)

    def insert_to_db(self):
        db = conn.get_db_conn()
        cur = db.cursor()
        id_company = self.find_id_company(cur)
        if id_company:
            return id_company
        cur.execute(
            "INSERT INTO companies (name, headquarters, rating, rating_count,"
            "benefits_rating, benefits_rating_count, nb_of_employees,"
            " founded, type, website, competitors) "
            "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
            (self.name, self.headquarters, self.rating, self.rating_count,
             self.benefits_rating, self.benefits_rating_count, self.size,
             self.founded, self.type,
             self.website, self.competitors))
        db.commit()
        return self.find_id_company(cur)

    def find_id_company(self, cur):
        cur.execute("SELECT id FROM companies where name = %s", (self.name,))
        exist = cur.fetchall()
        if len(exist) == 1:
            return exist[0][0]
        return None

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
    c1 = Company("Facebook", headquarters="Palo alto", benefits_rating=3.4,
                 benefits_rating_count=120,
                 founded=2004, type="Software",
                 website="https://www.facebook.com", rating=4,
                 rating_count=124)
    print(c1)


if __name__ == '__main__':
    main()