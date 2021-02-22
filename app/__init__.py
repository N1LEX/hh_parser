import httpx

BASE_URL = "https://api.hh.ru/vacancies/"
DEFAULT_ERRORS = httpx.RequestError, httpx.HTTPStatusError, httpx.HTTPError
