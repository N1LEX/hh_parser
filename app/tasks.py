from hh_parser.celery import app
from app.services import HHVacanciesParser


@app.task
def get_and_create_vacancies(page: int) -> None:
    """
    The task calls parse_vacancies_by_page method
    :param page: page number
    """
    hh_parser = HHVacanciesParser()
    hh_parser.parse_vacancies_by_page(page)
