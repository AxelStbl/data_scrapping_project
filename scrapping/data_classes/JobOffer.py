import scrapping.data_classes.Company as Company

ATTRIBUTES_TO_STRING = dict(job_id="ID", city="City", position="Job Title",
                            company="Company",
                            description="Description")


class JobOffer:
    def __init__(self, job_id, city=None, position=None, company=None,
                 description=None):
        """
        :param job_id: id found on the website
        :param city: city where the job offer is
        :param position: job position
        :param company: name of the company
        :param description: description found
        """
        self.job_id = job_id
        self.city = city
        self.company = company
        self.position = position
        self.company = company
        self.description = description

    def insert_to_db(self, company_id, db):
        """
        insert to db the job offer with the link to the company
        :param db: the database
        :param company_id: the id in db of the company
        """
        cur = db.cursor()
        # We are continuously improving our scrapping so on
        # duplicate key we can update the data we have
        cur.execute(
            "INSERT INTO job_offers "
            "(job_id, city, position, company_id, description) "
            "VALUES (%s, %s, %s, %s, %s)"
            "ON DUPLICATE KEY UPDATE city=%s, position = %s,"
            " description = %s",
            (self.job_id, self.city, self.position, company_id,
             self.description, self.city, self.position,
             self.description))
        db.commit()

    def __repr__(self):
        """
        aggregate in a nice manner the job offer
        :return: the string of the result
        """
        res = "Job offer :\n"
        res += "--------------\n"
        for var in vars(self):
            if self.__getattribute__(var):
                if var != "company":
                    res += ATTRIBUTES_TO_STRING[var] + ": " + \
                           str(self.__getattribute__(var)) + "\n"
        if self.company:
            res += '\t\n'.join(self.company.__repr__().splitlines())
        return res


def print_jobs(jobs):
    """
    Print all the jobs given in parameters
    :param jobs: the given jobs
    """
    print("All recent job offers are parsed showing the complete results: "
          "\n======================================\n")
    for job in jobs:
        print(job)
        print("----------")


def main():
    test = JobOffer(1, "paris", "Software Engineer",
                    Company.Company("Channel",
                                    rating="Rating",
                                    benefits_rating=4.5), None)
    print(test)


if __name__ == '__main__':
    main()
