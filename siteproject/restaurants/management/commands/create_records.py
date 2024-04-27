from django.core.management.base import BaseCommand
from restaurants.models import (Kitchen, VisitPurpose, Feature, District, Type)


class Command(BaseCommand):
    help = 'Creates records in the database'

    def handle(self, *args, **options):
        # Создаем начальные записи для Kitchen
        Kitchen.objects.bulk_create([
            Kitchen(name='Итальянская'),
            Kitchen(name='Русская'),
            Kitchen(name='Японская'),
            # Добавьте сколько угодно записей
        ])

        # Создаем начальные записи для VisitPurpose
        VisitPurpose.objects.bulk_create([
            VisitPurpose(name='Бизнес-ланч'),
            VisitPurpose(name='Романтическая встреча'),
            VisitPurpose(name='Деловая встреча'),
            # Добавьте сколько угодно записей
        ])

        # Создаем начальные записи для Feature
        Feature.objects.bulk_create([
            Feature(name='WiFi'),
            Feature(name='Барная стойка'),
            Feature(name='Бесплатная парковка'),
            # Добавьте сколько угодно записей
        ])

        # Создаем начальные записи для District
        District.objects.bulk_create([
            District(name='Авиастроительный район'),
            District(name='Вахитовский район'),
            District(name='Кировский район'),
            District(name='Московский район'),
            District(name='Ново-Савиновский район'),
            District(name='Приволжский район'),
            District(name='Советский район'),
            # Добавьте сколько угодно записей
        ])

        # Создаем начальные записи для Type
        Type.objects.bulk_create([
            Type(name='Ресторан'),
            Type(name='Кафе'),
            Type(name='Кофейная'),
            # Добавьте сколько угодно записей
        ])