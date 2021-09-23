from dataclasses import dataclass

from typing import List


@dataclass
class PageParser:
    page_data: dict

    def collect_vacancies_ids(self) -> List[int]:
        """
        The method collects and returns list of vacancies's ids
        It needs to get a full info about every vacancy
        :return: list of vacancies ids
        """
        return [vacancy['id'] for vacancy in self.page_data['items']]
