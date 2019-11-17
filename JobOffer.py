import Company

ATTRIBUTES_TO_STRING = dict(job_id="ID", city="City", position="Job Title", company="Company",
                            description="Description", salary="Salary")


class JobOffer:
    def __init__(self, job_id, city=None, position=None, company=None, description=None, salary=None):
        self.job_id = job_id
        self.company = company
        self.position = position
        self.company = company
        self.description = description
        self.salary = salary

    def __repr__(self):
        res = "Job offer :\n"
        res += "--------------\n"
        for var in vars(self):
            if self.__getattribute__(var):
                if var == "company":
                    res += '\t\n'.join(self.company.__repr__().splitlines())
                else:
                    res += ATTRIBUTES_TO_STRING[var] + ": " + str(self.__getattribute__(var)) + "\n"
        return res


def main():
    test = JobOffer(1, "paris", "Software Engineer",
                    Company.Company("Channel", headquarter_loc="Paris", rating="Rating", benefits_rating=4.5), None,
                    salary=5000)
    print(test)


if __name__ == '__main__':
    main()
