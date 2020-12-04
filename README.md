# hh_parser

Simple hh.ru vacancies data parser 


1. pip install -r requirements.txt
2. python manage.py migrate
3. redis-server
4. celery -A hh_parser.celery.app worker -l INFO
5. python manage.py collect_vacancies

