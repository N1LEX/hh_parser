from typing import List

from app.models import Vacancy


class VacancyHandler:

    @classmethod
    def save_vacancies(cls, vacancies: List[dict]):
        """
        Save vacancies to database.
        """
        for vacancy in vacancies:
            Vacancy.objects.get_or_create(**vacancy)
