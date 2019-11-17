ATTRIBUTES_TO_STRING = dict(name="Name", headquarters_loc="Headquarters localisation", rating="Rating",
                            rating_count="Total ratings",
                            benefits_rating="Benefits Rating",
                            benefits_rating_count="Benefits Rating Total Count",
                            size="Size", year_foundation="Year foundation",
                            company_type="Company Type", website="Website")


class Company:
    def __init__(self, name, headquarter_loc=None, rating=None, rating_count=None, benefits_rating=None,
                 benefits_rating_count=None, size=None, year_foundation=None,
                 company_type=None, website=None):
        self.name = name
        self.headquarters_loc = headquarter_loc
        self.rating = rating
        self.rating_count = rating_count
        self.benefits_rating = benefits_rating
        self.benefits_rating_count = benefits_rating_count
        self.size = size
        self.year_foundation = year_foundation
        self.company_type = company_type
        self.website = website

    def __repr__(self):
        res = "Company: \n"
        for var in vars(self):
            if self.__getattribute__(var):
                res += "\t" + ATTRIBUTES_TO_STRING[var] + ": " + str(self.__getattribute__(var)) + "\n"
        return res


def main():
    c1 = Company("Facebook", headquarter_loc="Palo alto", benefits_rating=3.4, benefits_rating_count=120,
                 year_foundation=2004, company_type="Software", website="https://www.facebook.com", rating=4,
                 rating_count=124)
    print(c1)


if __name__ == '__main__':
    main()
