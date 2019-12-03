import scrapping.conf.connector_db as conn
import scrapping.data_classes.Company as Company

ATTRIBUTES_TO_STRING = dict(job_id="ID", city="City", position="Job Title",
                            company="Company",
                            description="Description", salary="Salary")


class JobOffer:
    def __init__(self, job_id, city=None, position=None, company=None,
                 description=None, salary=None):
        """
        :param job_id: id found on the website
        :param city: city where the job offer is
        :param position: job position
        :param company: name of the company
        :param description: description found
        :param salary: average salary
        """
        self.job_id = job_id
        self.city = city
        self.company = company
        self.position = position
        self.company = company
        self.description = description
        self.salary = salary

    def insert_to_db(self, company_id):
        db = conn.get_db_conn()
        cur = db.cursor()
        # We are continuously improving our scrapping so on
        # duplicate key we can update the data we have
        cur.execute(
            "INSERT INTO job_offers "
            "(job_id, city, position, company_id, description, salary) "
            "VALUES (%s, %s, %s, %s, %s, %s)"
            "ON DUPLICATE KEY UPDATE city=%s, position = %s,"
            " description = %s, salary = %s",
            (self.job_id, self.city, self.position, company_id,
             self.description, self.salary, self.city, self.position,
             self.description, self.salary))
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
                if var == "company":
                    res += '\t\n'.join(self.company.__repr__().splitlines())
                else:
                    res += ATTRIBUTES_TO_STRING[var] + ": " + \
                           str(self.__getattribute__(var)) + "\n"
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
                    Company.Company("Channel", headquarters="Paris",
                                    rating="Rating",
                                    benefits_rating=4.5), None,
                    salary=5000)
    print(test)


if __name__ == '__main__':
    main()
