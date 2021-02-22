from django.core.management import BaseCommand

from app.tasks import init_search


class Command(BaseCommand):

    def handle(self, *args, **options):
        """
        Command runs a collect of vacancies data from hh.ru
        For an every page creates a celery task

        To run a data's collect:
        python manage.py collect_vacancies
        """
        init_search.delay()
