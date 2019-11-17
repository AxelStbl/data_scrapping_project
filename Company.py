ATTRIBUTES_TO_STRING = dict(name="Name", headquarters="Headquarters localisation", rating="Rating",
                            rating_count="Total ratings",
                            benefits_rating="Benefits Rating",
                            benefits_rating_count="Benefits Rating Total Count",
                            size="Size", founded="Year foundation",
                            type="Company Type", website="Website", competitors="Competitors")


class Company:
    def __init__(self, name, headquarters=None, rating=None, rating_count=None, benefits_rating=None,
                 benefits_rating_count=None, size=None, founded=None,
                 type=None, website=None, competitors=None):
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
        """replace all values by their corresponding value"""
        for key, value in data_dict.items():
            if key in vars(self):
                self[key] = value

    def __setitem__(self, key, value):
        self.__setattr__(key, value)

    def __repr__(self):
        res = "Company: \n"
        for var in vars(self):
            if self.__getattribute__(var):
                res += "\t" + ATTRIBUTES_TO_STRING[var] + ": " + str(self.__getattribute__(var)) + "\n"
        return res


def main():
    c1 = Company("Facebook", headquarters="Palo alto", benefits_rating=3.4, benefits_rating_count=120,
                 founded=2004, type="Software", website="https://www.facebook.com", rating=4,
                 rating_count=124)
    print(c1)


if __name__ == '__main__':
    main()
