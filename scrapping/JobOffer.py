from scrapping import *

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
        self.company = company
        self.position = position
        self.company = company
        self.description = description
        self.salary = salary

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
                    Company("Channel", headquarters="Paris",
                            rating="Rating",
                            benefits_rating=4.5), None,
                    salary=5000)
    print(test)


if __name__ == '__main__':
    main()
