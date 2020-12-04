import httpx
from typing import List

from app.models import Vacancy


class HHVacanciesParser:
    """
    Class implements a collect of vacancies data from hh.ru and
    saves them to database
    """
    BASE_VACANCIES_URL = "https://api.hh.ru/vacancies/"

    def get_vacancies(self, page: int = 1) -> dict:
        """
        Retrieves all vacancies on the page
        :return: vacancies data
        """
        params = dict(page=page)
        response = httpx.get(self.BASE_VACANCIES_URL, params=params)
        return response.json()

    def get_vacancy(self, vacancy_id: int) -> dict:
        """
        Retrieve a vacancy by id
        :param vacancy_id: int
        :return: vacancy data
        """
        vacancy_url = f"{self.BASE_VACANCIES_URL}{vacancy_id}"
        response = httpx.get(vacancy_url)
        return response.json()

    def get_total_pages(self) -> int:
        """
        Method retrieves a count of pages for available to collect
        :return: total pages
        """
        response = self.get_vacancies()
        return response.get("pages", 0)

    @staticmethod
    def get_vacancies_ids(vacancies: dict) -> List[int]:
        """
        Method collect and return list of vacancies's ids
        This need to get a full info on an every vacancy
        :return: list of vacancies ids
        """
        return [vacancy["id"] for vacancy in vacancies["items"]]

    @staticmethod
    def get_salary_value(raw_salary: dict) -> str or None:
        """
        Generate a salary value from fields
        :param raw_salary: dict
        :return: generated value or None
        """
        if not raw_salary:
            return None

        salary_from = raw_salary['from']
        salary_to = raw_salary['to']
        currency = raw_salary['currency']
        gross = "до вычета налогов" if raw_salary["gross"] else "на руки"

        if salary_from and not salary_to:
            salary = f"от {salary_from}"
        elif salary_to and not salary_from:
            salary = f"до {salary_to}"
        else:
            salary = f"{salary_from}-{salary_to}"

        full_salary_info = " ".join([salary, currency, gross])
        return full_salary_info

    @staticmethod
    def get_key_skills(key_skills) -> str:
        """
        Generate a value for key skills field
        :param key_skills: list
        :return: a joined elements to string
        """
        skills = [skill["name"] for skill in key_skills]
        return ", ".join(skills)

    def prepare_vacancy_data(self, raw_vacancy: dict) -> dict:
        """Preparing vacancy data before save to database"""
        vacancy_data = dict(
            name=raw_vacancy["name"],
            description=raw_vacancy["description"],
            key_skills=self.get_key_skills(raw_vacancy["key_skills"]),
            salary=self.get_salary_value(raw_vacancy["salary"]),
            link=raw_vacancy["alternate_url"],
        )
        return vacancy_data

    @staticmethod
    def save_vacancies(vacancies: List[Vacancy]) -> None:
        """
        Method saves list of Vacancy's instances to database
        :param vacancies: list of Vacancy instances
        """
        Vacancy.objects.bulk_create(vacancies)

    def parse_vacancies_by_page(self, page: int) -> None:
        """
        Method retrieves all vacancies on the page,
        collects info by every vacancy and adds it to a list for save
        in result saves all instances to database
        :param page: page number
        """
        vacancies = self.get_vacancies(page)
        vacancies_ids = self.get_vacancies_ids(vacancies)
        vacancy_instances = []

        for vacancy_id in vacancies_ids:
            raw_vacancy_data = self.get_vacancy(vacancy_id)
            vacancy_data = self.prepare_vacancy_data(raw_vacancy_data)
            vacancy = Vacancy(**vacancy_data)
            vacancy_instances.append(vacancy)

        self.save_vacancies(vacancy_instances)
