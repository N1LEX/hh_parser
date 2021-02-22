from typing import List

import httpx
from celery import chord

from app import DEFAULT_ERRORS, BASE_URL
from app.handlers.vacancy import VacancyHandler
from app.parsers.page import PageParser
from app.parsers.search import SearchParser
from app.parsers.vacancy import VacancyParser
from hh_parser.celery import app


@app.task(ignore_result=True, autoretry_for=DEFAULT_ERRORS, retry_kwargs={'max_retries': 10, 'countdown': 15})
def init_search():
    """
    Init parse data.
    """
    response = httpx.get(BASE_URL).json()
    total_pages = SearchParser(response).get_total_pages()
    for page in range(total_pages):
        load_page.delay(page)


@app.task(ignore_result=True, autoretry_for=DEFAULT_ERRORS, retry_kwargs={'max_retries': 10, 'countdown': 15})
def load_page(page: int):
    """
    Collect and save page data.
    """
    response = httpx.get(BASE_URL, params={'page': page}).json()
    vacancies_ids = PageParser(response).collect_vacancies_ids()
    tasks = [collect_vacancy.s(vacancy_id) for vacancy_id in vacancies_ids]
    chord(tasks, save_vacancies.s())()


@app.task(ignore_result=True, autoretry_for=DEFAULT_ERRORS, retry_kwargs={'max_retries': 10, 'countdown': 15})
def collect_vacancy(vacancy_id: int) -> dict:
    """
    Collect vacancy data.
    """
    vacancy_url = BASE_URL + vacancy_id
    response = httpx.get(vacancy_url).json()
    return VacancyParser(response).collect_vacancy()


@app.task(ignore_result=True)
def save_vacancies(vacancies: List[dict]):
    """
    Save vacancies to database.
    """
    VacancyHandler.save_vacancies(vacancies)
