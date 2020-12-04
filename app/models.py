from django.db import models


class Vacancy(models.Model):
    name = models.CharField("Наименование", max_length=255)
    description = models.TextField("Описание вакансии")
    key_skills = models.TextField("Ключевые навыки", null=True)
    salary = models.CharField("Заработная плата", null=True, max_length=25)
    link = models.CharField("Ссылка на вакансию", max_length=255)

    class Meta:
        verbose_name = "Вакансия"
        verbose_name_plural = "Вакансии"

    def __str__(self):
        return self.name
