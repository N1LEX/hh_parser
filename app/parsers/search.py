from dataclasses import dataclass


@dataclass
class SearchParser:
    response: dict

    def get_total_pages(self) -> int:
        """
        Method retrieves a count of pages for available to collect
        :return: total pages
        """
        return self.response.get('pages', 0)
