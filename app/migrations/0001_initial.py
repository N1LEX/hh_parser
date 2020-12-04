# Generated by Django 3.1.4 on 2020-12-04 19:21

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Vacancy',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Наименование')),
                ('description', models.TextField(verbose_name='Описание вакансии')),
                ('key_skills', models.TextField(null=True, verbose_name='Ключевые навыки')),
                ('salary', models.CharField(max_length=25, null=True, verbose_name='Заработная плата')),
                ('link', models.CharField(max_length=255, verbose_name='Ссылка на вакансию')),
            ],
            options={
                'verbose_name': 'Вакансия',
                'verbose_name_plural': 'Вакансии',
            },
        ),
    ]
