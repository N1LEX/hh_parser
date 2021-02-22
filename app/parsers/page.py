from dataclasses import dataclass

from typing import List


@dataclass
class PageParser:
    page_data: dict

    def collect_vacancies_ids(self) -> List[int]:
        """
        Method collect and return list of vacancies's ids
        This need to get a full info on an every vacancy
        :return: list of vacancies ids
        """
        return [vacancy['id'] for vacancy in self.page_data['items']]
