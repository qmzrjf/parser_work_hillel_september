class Vacancy:
    vacancy_id: int
    title: str
    href: str

    def to_list(self):
        return [self.vacancy_id, self.title, self.href]

    def to_dict(self):
        return {
            "vacancyId": self.vacancy_id,
            "title": self.title,
            "href": self.href
        }
