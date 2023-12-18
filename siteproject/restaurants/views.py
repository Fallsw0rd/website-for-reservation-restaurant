from django.contrib.auth.decorators import user_passes_test, login_required
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView, UpdateView, CreateView
from django.shortcuts import get_object_or_404
from django.db import models
from .forms import RestaurantForm, WorkTimeForm, ReservationForm, ReviewForm
from .models import Restaurant, WorkTime, Table, Reservation, Review
from main.models import CustomUser
from django.http import JsonResponse
from datetime import datetime, timedelta


# Проверка пользователя на админа
def user_is_admin(user):
    return user.is_authenticated and user.is_staff


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


# Редактирование ресторана админом и владельцем ресторана
class RestaurantUpdateView(UserPassesTestMixin, UpdateView):
    model = Restaurant
    form_class = RestaurantForm
    template_name = 'restaurants/profile_create.html'
    success_url = reverse_lazy('main')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        restaurant = self.get_object()

        # Получаем информацию о WorkTime ресторана
        work_time = WorkTime.objects.get(restaurant=restaurant)
        work_time_form = WorkTimeForm(instance=work_time)

        context['work_time_form'] = work_time_form
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        work_time_form = context['work_time_form']

        if form.is_valid() and work_time_form.is_valid():
            self.object = form.save()
            return super().form_valid(form)

        return self.form_invalid(form)

    def test_func(self):
        restaurant = self.get_object()
        return self.request.user.is_authenticated and (
                    self.request.user.is_staff or self.request.user == restaurant.owner)

    def handle_no_permission(self):
        return redirect('main')


# Создание нового ресторана админом
@user_passes_test(user_is_admin)
def create_restaurant(request):
    if request.method == 'POST':
        restaurant_form = RestaurantForm(request.POST, request.FILES, initial={'owner': request.user})
        work_time_form = WorkTimeForm(request.POST)

        if restaurant_form.is_valid() and work_time_form.is_valid():
            restaurant = restaurant_form.save()

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
    print(user)
    if request.method == 'POST':
        print('post')
        form = ReviewForm(request.POST, user_name=user, initial={'user': user})
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
