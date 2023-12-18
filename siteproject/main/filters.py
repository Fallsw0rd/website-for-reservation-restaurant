from django import forms
import django_filters
from restaurants.models import District, Feature, Kitchen, Restaurant
from django.db.models import Q


class AverageCheckFilter(django_filters.ChoiceFilter):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.extra['choices'] = [
            (0, 'до 1000'),
            (1000, '1000-2000'),
            (2000, '2000-3000'),
            (3000, 'от 3000'),
        ]

    def filter(self, qs, value):
        if value:
            value = int(value)
            if value == 0:
                return qs.filter(Q(min_average_check__lte=1000) | Q(max_average_check__lte=1000))
            elif value == 1000:
                return qs.filter(
                    Q(min_average_check__gte=1000, min_average_check__lte=2000) | Q(max_average_check__gte=1000,
                                                                                    max_average_check__lte=2000))
            elif value == 2000:
                return qs.filter(
                    Q(min_average_check__gte=2000, min_average_check__lte=3000) | Q(max_average_check__gte=2000,
                                                                                    max_average_check__lte=3000))
            elif value == 3000:
                return qs.filter(Q(min_average_check__gte=3000) | Q(max_average_check__gte=3000))
        return qs


class RestaurantFilter(django_filters.FilterSet):
    district = django_filters.ModelChoiceFilter(
        field_name='district',
        queryset=District.objects.all(),
        label='Район',
    )

    features = django_filters.ModelMultipleChoiceFilter(
        field_name='features',
        queryset=Feature.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        label='Особенности',
        conjoined = True,
    )

    kitchens = django_filters.ModelMultipleChoiceFilter(
        field_name='kitchens',
        queryset=Kitchen.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        label='Кухни',
        conjoined=True,
    )

    average_check = AverageCheckFilter(
        field_name='min_average_check',
        label='Средний чек',
    )

    class Meta:
        model = Restaurant
        fields = ['district', 'features', 'kitchens', 'average_check']


