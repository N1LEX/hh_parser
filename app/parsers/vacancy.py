from dataclasses import dataclass
from typing import Union


@dataclass
class VacancyParser:
    vacancy_data: dict

    def collect_vacancy(self) -> dict:
        """Collect vacancy data."""
        return dict(
            name=self.vacancy_data.get("name"),
            description=self.vacancy_data.get("description"),
            key_skills=self._get_key_skills(),
            salary=self._get_salary_value(),
            link=self.vacancy_data.get("alternate_url"),
        )

    def _get_key_skills(self) -> str:
        """
        Generate a value for key skills field
        :return: a joined elements to string
        """
        skills = [skill['name'] for skill in self.vacancy_data.get('key_skills')]
        return ', '.join(skills)

    def _get_salary_value(self) -> Union[str, None]:
        """
        Generate a salary value from fields
        :return: generated value or None
        """
        return self._handle_salary_value() if self.vacancy_data.get('salary') else None

    def _handle_salary_value(self) -> str:
        """Handle and return salary info"""
        salary_info = self.vacancy_data.get('salary')
        salary_from = salary_info['from']
        salary_to = salary_info['to']
        currency = salary_info['currency']
        gross = 'до вычета налогов' if salary_info['gross'] else 'на руки'

        if salary_from and not salary_to:
            salary = f'от {salary_from}'
        elif salary_to and not salary_from:
            salary = f'до {salary_to}'
        else:
            salary = f'{salary_from}-{salary_to}'

        return ' '.join([salary, currency, gross])
