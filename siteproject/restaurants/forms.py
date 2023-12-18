from django import forms
from .models import Restaurant, Kitchen, WorkTime, VisitPurpose, Feature, District, Type, Reservation, Review
from datetime import datetime, timedelta, date


class KitchenForm(forms.ModelForm):
    class Meta:
        model = Kitchen
        fields = ['name']


class TypeForm(forms.ModelForm):
    class Meta:
        model = Type
        fields = ['name']


class VisitPurposeForm(forms.ModelForm):
    class Meta:
        model = VisitPurpose
        fields = ['name']


class FeatureForm(forms.ModelForm):
    class Meta:
        model = Feature
        fields = ['name']


class DistrictForm(forms.ModelForm):
    class Meta:
        model = District
        fields = ['name']


class WorkTimeForm(forms.ModelForm):
    class Meta:
        model = WorkTime
        fields = [
            'monday_opening_time', 'monday_closing_time',
            'tuesday_opening_time', 'tuesday_closing_time',
            'wednesday_opening_time', 'wednesday_closing_time',
            'thursday_opening_time', 'thursday_closing_time',
            'friday_opening_time', 'friday_closing_time',
            'saturday_opening_time', 'saturday_closing_time',
            'sunday_opening_time', 'sunday_closing_time',
        ]
        widgets = {
            'monday_opening_time': forms.TimeInput(format='%H:%M', attrs={'type': 'time'}),
            'monday_closing_time': forms.TimeInput(format='%H:%M', attrs={'type': 'time'}),
            'tuesday_opening_time': forms.TimeInput(format='%H:%M', attrs={'type': 'time'}),
            'tuesday_closing_time': forms.TimeInput(format='%H:%M', attrs={'type': 'time'}),
            'wednesday_opening_time': forms.TimeInput(format='%H:%M', attrs={'type': 'time'}),
            'wednesday_closing_time': forms.TimeInput(format='%H:%M', attrs={'type': 'time'}),
            'thursday_opening_time': forms.TimeInput(format='%H:%M', attrs={'type': 'time'}),
            'thursday_closing_time': forms.TimeInput(format='%H:%M', attrs={'type': 'time'}),
            'friday_opening_time': forms.TimeInput(format='%H:%M', attrs={'type': 'time'}),
            'friday_closing_time': forms.TimeInput(format='%H:%M', attrs={'type': 'time'}),
            'saturday_opening_time': forms.TimeInput(format='%H:%M', attrs={'type': 'time'}),
            'saturday_closing_time': forms.TimeInput(format='%H:%M', attrs={'type': 'time'}),
            'sunday_opening_time': forms.TimeInput(format='%H:%M', attrs={'type': 'time'}),
            'sunday_closing_time': forms.TimeInput(format='%H:%M', attrs={'type': 'time'}),
        }


class RestaurantForm(forms.ModelForm):
    kitchens = forms.ModelMultipleChoiceField(
        queryset=Kitchen.objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )
    visit_purposes = forms.ModelMultipleChoiceField(
        queryset=VisitPurpose.objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )
    features = forms.ModelMultipleChoiceField(
        queryset=Feature.objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )
    district = forms.ModelChoiceField(
        queryset=District.objects.all(),
    )

    class Meta:
        model = Restaurant
        fields = ['name', 'address', 'contact_number', 'description',
                  'restaurant_image', 'photo_1', 'photo_2', 'photo_3',
                  'min_average_check', 'max_average_check', 'district', 'features', 'visit_purposes', 'type',
                  'kitchens', 'owner']

    def clean_contact_number(self):
        contact_number = self.cleaned_data['contact_number']
        if Restaurant.objects.filter(contact_number=contact_number).exists():
            raise forms.ValidationError("Ресторан с таким контактным номером уже существует.")
        return contact_number


class FilterCheckForm(forms.Form):
    check_range = forms.ChoiceField(
        choices=[
            ('', 'Цена'),
            ('0', 'до 1000'),
            ('1', '1000-2000'),
            ('2', '2000-3000'),
            ('3', 'от 3000')
        ], required=False)


class ReservationForm(forms.ModelForm):

    def __init__(self, *args, restaurant=None, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.restaurant = restaurant
        self.fields['date'].initial = date.today().strftime('%Y-%m-%d')

        if user:
            self.fields['name'].initial = user.surname + ' ' + user.name + ' ' + user.middlename
            self.fields['phone'].initial = user.phone_number

        # Добавляем логику для создания choices в поле времени на основе графика работы ресторана
        if restaurant:
            # Получите значение даты из формы
            selected_date = self.data.get('date') or self.fields['date'].initial
            work_time = WorkTime.objects.get(restaurant=restaurant)
            choices = self.get_time_choices(work_time, selected_date)
            self.fields['time'].widget.choices = choices

    def get_time_choices(self, work_time, selected_date):
        choices = []
        current_day_of_week = datetime.strptime(selected_date, '%Y-%m-%d').strftime('%A').lower()

        opening_time_attr = f'{current_day_of_week}_opening_time'
        closing_time_attr = f'{current_day_of_week}_closing_time'

        opening_time = getattr(work_time, opening_time_attr, None)
        closing_time = getattr(work_time, closing_time_attr, None)

        current_datetime = datetime.combine(datetime.strptime(selected_date, '%Y-%m-%d'), opening_time)

        if closing_time < opening_time:
            closing_time = datetime.combine(datetime.strptime(selected_date, '%Y-%m-%d') + timedelta(days=1), closing_time)

            while current_datetime < closing_time:
                choices.append((current_datetime.strftime('%H:%M'), current_datetime.strftime('%H:%M')))
                current_datetime += timedelta(minutes=30)
        else:
            while current_datetime.time() < closing_time:
                choices.append((current_datetime.strftime('%H:%M'), current_datetime.strftime('%H:%M')))
                current_datetime += timedelta(minutes=30)

        return choices

    class Meta:
        model = Reservation
        fields = ['date', 'time', 'name', 'phone', 'additional_info', 'count_guess']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'time': forms.Select(),
        }


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['reviewer_name', 'comment', 'rating', 'user']

    RATING_CHOICES = [(i, int(i)) for i in range(1, 6)]  # Опции рейтинга от 1 до 5

    rating = forms.ChoiceField(
        choices=RATING_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Оценка'
    )

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user_name', None)
        super(ReviewForm, self).__init__(*args, **kwargs)
        if user:
            self.fields['reviewer_name'].initial = f'{user.name} {user.surname}'
