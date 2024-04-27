from django.contrib.auth.decorators import user_passes_test, login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView, CreateView, ListView
from django.shortcuts import get_object_or_404
from django.db import models
from .forms import RestaurantForm, WorkTimeForm, ReservationForm, ReviewForm, TableCreationForm
from .models import Restaurant, WorkTime, Table, Reservation, Review, TableAdditionRequest, MapAdditionRequest
from main.models import CustomUser
from django.http import JsonResponse
from datetime import datetime, timedelta, date
from babel.dates import format_date


# Проверка пользователя на админа
def user_is_admin(user):
    return user.is_authenticated and (user.is_staff or user.groups.filter(name='Владельцы').exists())


def statistics(request, name, pk):
    restaurant = get_object_or_404(Restaurant, pk=pk)
    if not (request.user.is_staff or request.user == restaurant.owner):
        return redirect('main')

    today = datetime.today()
    current_year = today.year
    years = range(current_year, current_year - 10, -1)

    option = request.GET.get('option')
    day = request.GET.get('day')
    month = request.GET.get('month')
    year = request.GET.get('year')

    reservations = Reservation.objects.filter(table__restaurant=restaurant)
    reviews = Review.objects.filter(restaurant=restaurant)
    if day:
        date_parts = day.split('-')
        day_year = int(date_parts[0])
        day_month = int(date_parts[1])
        day_day = int(date_parts[2])

        # Фильтрация по дате
        reservations = reservations.filter(date__year=day_year, date__month=day_month, date__day=day_day)
        reviews = reviews.filter(created_at__year=day_year, created_at__month=day_month, created_at__day=day_day)
    if month:
        month_number = int(month.split("-")[1]) if "-" in month else int(month)
        if 1 <= month_number <= 12:
            reservations = reservations.filter(date__month=month_number)
            reviews = reviews.filter(created_at__month=month_number)
    if year:
        reservations = reservations.filter(date__year=year)
        reviews = reviews.filter(created_at__year=year)

    if option:
        if option == 'day':
            option = f'Статистика по дню {day}'
        elif option == 'month':
            year, month_number = map(int, month.split('-'))
            month_name = format_date(date(year, month_number, 1), "MMMM yyyy", locale='ru_RU').capitalize()
            option = f'Статистика с {month_name}'
        elif option == 'year':
            option = f'Статистика за {year} год'
        else:
            option = 'Статистика по бронированиям'

    reservations_count = reservations.count()
    reservation_success = reservations.filter(is_accepted=True).count()
    reservation_cancelled = reservations.filter(is_cancelled=True).count()
    reviews_count = reviews.count()
    average_rating = reviews.aggregate(avg_rating=models.Avg('rating'))['avg_rating']

    context = {
        'restaurant': restaurant,
        'reservations_count': reservations_count,
        'reviews_count': reviews_count,
        'average_rating': average_rating,
        'reservation_success': reservation_success,
        'reservation_cancelled': reservation_cancelled,
        'years': years,
        'option': option,
    }
    return render(request, 'restaurants/statistics.html', context)


class MyRestaurants(ListView):
    template_name = 'restaurants/my_restaurants.html'
    context_object_name = 'restaurants'

    def get_queryset(self):
        return Restaurant.objects.filter(owner=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_day_of_week = datetime.now().strftime('%A')
        restaurants = context['restaurants']
        for restaurant in restaurants:
            work_time = WorkTime.objects.get(restaurant=restaurant)
            if work_time:
                if current_day_of_week == 'Monday':
                    restaurant.opening_time = work_time.monday_opening_time
                    restaurant.closing_time = work_time.monday_closing_time
                elif current_day_of_week == 'Tuesday':
                    restaurant.opening_time = work_time.tuesday_opening_time
                    restaurant.closing_time = work_time.tuesday_closing_time
                elif current_day_of_week == 'Wednesday':
                    restaurant.opening_time = work_time.wednesday_opening_time
                    restaurant.closing_time = work_time.wednesday_closing_time
                elif current_day_of_week == 'Thursday':
                    restaurant.opening_time = work_time.thursday_opening_time
                    restaurant.closing_time = work_time.thursday_closing_time
                elif current_day_of_week == 'Friday':
                    restaurant.opening_time = work_time.friday_opening_time
                    restaurant.closing_time = work_time.friday_closing_time
                elif current_day_of_week == 'Saturday':
                    restaurant.opening_time = work_time.saturday_opening_time
                    restaurant.closing_time = work_time.saturday_closing_time
                else:
                    restaurant.opening_time = work_time.sunday_opening_time
                    restaurant.closing_time = work_time.sunday_closing_time
        return context


# Профиль ресторана
class RestaurantDetailView(DetailView):
    model = Restaurant
    template_name = 'restaurants/profile_rest.html'
    context_object_name = 'restaurant'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        restaurant = self.get_object()
        tables = Table.objects.filter(restaurant=restaurant)
        work_time = WorkTime.objects.get(restaurant=restaurant)
        reviews = Review.objects.filter(restaurant_id=restaurant)
        average_rating = reviews.aggregate(models.Avg('rating'))['rating__avg']

        context['average_rating'] = average_rating
        context['is_admin'] = self.request.user.is_authenticated and self.request.user.is_staff
        context['work_time'] = work_time
        context['tables'] = tables
        context['reviews'] = reviews

        return context


# Создание новой брони пользователем у ресторана
@method_decorator(login_required, name='dispatch')
class ReservationCreateView(LoginRequiredMixin, CreateView):
    model = Reservation
    form_class = ReservationForm
    template_name = 'restaurants/reservation.html'

    def get_queryset(self):
        restaurant_id = self.kwargs.get('pk')
        return Table.objects.filter(restaurant_id=restaurant_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        restaurant_id = self.kwargs.get('pk')
        user = self.request.user
        restaurant = Restaurant.objects.get(pk=restaurant_id)
        tables = Table.objects.filter(restaurant_id=restaurant_id)

        context['user'] = user
        context['tables'] = tables
        context['restaurant'] = restaurant
        context['reservation_form'] = self.form_class(restaurant=restaurant, user=user)

        return context

    @csrf_exempt
    def form_valid(self, form):
        user_id = self.request.POST.get('user')
        table_id = self.request.POST.get('table')

        user = get_object_or_404(CustomUser, id=user_id)
        table = get_object_or_404(Table, id=table_id)

        form.instance.user = user
        form.instance.table = table

        response = super().form_valid(form)

        table.save()

        messages.success(self.request, 'Столик забронирован, посмотрите в своем профиле его подтверждение рестораном')

        return response

    def get_success_url(self):
        return reverse('main')


# Проверка наличия брони на стол
def check_reservation(request):
    if request.method == 'POST':
        table_id = request.POST.get('table_id')
        date = request.POST.get('date')
        time = request.POST.get('time')
        is_reserved = Reservation.objects.filter(table_id=table_id, date=date, time=time).exists()
        return JsonResponse({'is_reserved': is_reserved})

    return JsonResponse({'error': 'Invalid request method'})


# Редактирование профиля ресторана админом и владельцем ресторана
@login_required
def update_restaurant(request, name, pk):
    restaurant = get_object_or_404(Restaurant, pk=pk)

    if not (request.user.is_staff or request.user == restaurant.owner):
        return redirect('main')

    work_time = restaurant.worktime

    if request.method == 'POST':
        restaurant_form = RestaurantForm(request.POST, request.FILES, instance=restaurant)
        work_time_form = WorkTimeForm(request.POST, instance=work_time)
        if restaurant_form.is_valid() and work_time_form.is_valid():
            restaurant_form.save()
            work_time_form.save()
            return redirect('restaurants:profile-rest', name=name, pk=pk)
    else:
        restaurant_form = RestaurantForm(instance=restaurant)
        work_time_form = WorkTimeForm(instance=work_time)

    context = {
        'form': restaurant_form,
        'work_time_form': work_time_form,
    }
    return render(request, 'restaurants/profile_create.html', context)


# Создание нового ресторана
@user_passes_test(user_is_admin)
def create_restaurant(request):
    if request.method == 'POST':
        restaurant_form = RestaurantForm(request.POST, request.FILES)
        work_time_form = WorkTimeForm(request.POST)
        if restaurant_form.is_valid() and work_time_form.is_valid():
            restaurant = restaurant_form.save(commit=False)
            restaurant.owner = request.user
            restaurant.save()

            work_time_form.instance.restaurant = restaurant
            work_time_form.save()

            return redirect('main')

    else:
        restaurant_form = RestaurantForm(initial={'owner': request.user})
        work_time_form = WorkTimeForm()

    return render(request, 'restaurants/profile_create.html',
                  {'form': restaurant_form, 'work_time_form': work_time_form})


# Создание отзыва ресторану пользователем
@login_required
def create_review(request, name, pk):
    restaurant = get_object_or_404(Restaurant, name=name, id=pk)
    user = request.user
    if request.method == 'POST':
        form = ReviewForm(request.POST, user_name=user, initial={'user': user})
        print(form.is_valid())
        print(user)
        print(form.errors)
        if form.is_valid():
            review = form.save(commit=False)
            review.restaurant = restaurant
            review.user = user
            review.save()
            return redirect('restaurants:profile-rest', name=name, pk=pk)
    else:
        form = ReviewForm(user_name=user)

    return render(request, 'restaurants/review_create.html',
                  {'user': user, 'form': form, 'restaurant': restaurant})


# Список броней для ресторана
def reservations_tables(request, name, pk):
    restaurant = get_object_or_404(Restaurant, name=name, id=pk)
    tables = Table.objects.filter(restaurant=restaurant)
    reservations = Reservation.objects.filter(table__restaurant=restaurant)

    return render(request, 'restaurants/list_tables.html',
                  {'restaurant': restaurant, 'tables': tables, 'reservations': reservations})


def map_update(request, name, pk):
    restaurant = get_object_or_404(Restaurant, pk=pk)
    if request.method == 'POST':
        form = TableCreationForm(request.POST, request.FILES)
        if form.is_valid():
            # Создаем новую заявку на добавление карты
            map_request = MapAdditionRequest.objects.create(restaurant=restaurant, photo=form.cleaned_data['photo'])
            num_tables = form.cleaned_data['num_tables']
            for i in range(num_tables):
                number = form.cleaned_data[f'number_{i}']
                capacity = form.cleaned_data[f'capacity_{i}']
                photo_table = form.cleaned_data[f'photo_{i}']
                # Создаем новую заявку на добавление стола, связанную с заявкой на добавление карты
                TableAdditionRequest.objects.create(map_request=map_request, number=number, capacity=capacity,
                                                    photo=photo_table)
            return redirect('restaurants:profile-rest', name=name, pk=pk)
    else:
        form = TableCreationForm()
    return render(request, 'restaurants/map_update.html', {'form': form, 'restaurant': restaurant})


# Подтверждение брони рестораном
def confirm_reservation(request, reservation_id):
    reservation = get_object_or_404(Reservation, pk=reservation_id)
    request.method = 'POST'
    if request.method == 'POST':
        reservation.is_accepted = True
        reservation.save()
        return JsonResponse({'status': 'success'})

    return JsonResponse({'status': 'error'})


# Отмена брони пользователем
def cancel_reservation(request, reservation_id):
    reservation = get_object_or_404(Reservation, pk=reservation_id)
    request.method = 'POST'
    if request.method == 'POST':
        reservation.is_cancelled = True
        reservation.save()
        return JsonResponse({'status': 'success'})

    return JsonResponse({'status': 'error'})


def get_time_choices(request):
    selected_date = request.GET.get('selected_date')
    work_time = WorkTime.objects.get(restaurant_id=request.GET.get('restaurant_id'))
    choices = get_updated_time_choices(work_time, selected_date)
    return JsonResponse({'choices': choices})


def get_updated_time_choices(work_time, selected_date):
    selected_datetime = datetime.strptime(selected_date, '%Y-%m-%d')

    current_day_of_week = selected_datetime.strftime('%A').lower()

    opening_time_attr = f'{current_day_of_week}_opening_time'
    closing_time_attr = f'{current_day_of_week}_closing_time'

    opening_time = getattr(work_time, opening_time_attr, None)
    closing_time = getattr(work_time, closing_time_attr, None)

    current_datetime = datetime.combine(selected_datetime, opening_time)
    choices = []

    if closing_time < opening_time:
        closing_time = datetime.combine(selected_datetime + timedelta(days=1), closing_time)

        while current_datetime < closing_time:
            choices.append((current_datetime.strftime('%H:%M')))
            current_datetime += timedelta(minutes=30)
    else:
        while current_datetime.time() < closing_time:
            choices.append((current_datetime.strftime('%H:%M')))
            current_datetime += timedelta(minutes=30)

    return choices
