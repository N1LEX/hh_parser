from django.core.management import BaseCommand

from app.services import HHVacanciesParser
from app.tasks import get_and_create_vacancies


class Command(BaseCommand):

    def handle(self, *args, **options):
        """
        Command runs a collect of vacancies data from hh.ru
        For an every page creates a celery task

        To run a data's collect:
        python manage.py collect_vacancies
        """
        hh_parser = HHVacanciesParser()
        total_pages = hh_parser.get_total_pages()

        for page in range(total_pages):
            get_and_create_vacancies.delay(page)
