from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.contrib.auth import login
from django.db.models import Q
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView
from django.contrib.messages.views import SuccessMessageMixin
from django.db import models
from .forms import CustomUserCreationForm, CustomUserLoginForm, ProfileEditForm, AvatarUploadForm
from restaurants.models import Restaurant, WorkTime, Kitchen, District, Feature, Reservation, Review
from publications.models import Publication
from .filters import RestaurantFilter


# Главная страница
def index(request):
    popular_restaurants = Restaurant.objects.annotate(average_rating=models.Avg('review__rating')).order_by(
        '-average_rating')[:9]
    publications = Publication.objects.all()
    current_day_of_week = datetime.now().strftime('%A')

    for restaurant in popular_restaurants:
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

    context = {
        'popular_restaurants': popular_restaurants,
        'publications': publications,
    }

    return render(request, 'main/index.html', context)


# Страница "Рестораны"
class RestaurantListView(ListView):
    model = Restaurant
    template_name = 'main/restaurants.html'
    context_object_name = 'restaurants'
    filterset_class = RestaurantFilter

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        all_restaurants = context['restaurants']
        current_day_of_week = datetime.now().strftime('%A').lower()

        for restaurant in all_restaurants:
            work_time = WorkTime.objects.get(restaurant=restaurant)

            if work_time:
                opening_time_attr = f'{current_day_of_week}_opening_time'
                closing_time_attr = f'{current_day_of_week}_closing_time'

                restaurant.opening_time = getattr(work_time, opening_time_attr, None)
                restaurant.closing_time = getattr(work_time, closing_time_attr, None)

            reviews = Review.objects.filter(restaurant=restaurant)
            average_rating = reviews.aggregate(models.Avg('rating'))['rating__avg']
            restaurant.average_rating = average_rating

        context['restaurants'] = all_restaurants
        context['kitchens'] = Kitchen.objects.all()
        context['districts'] = District.objects.all()
        context['features'] = Feature.objects.all()
        context['filter'] = self.filterset_class(self.request.GET, queryset=self.get_queryset())

        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        return self.filterset_class(self.request.GET, queryset=queryset).qs


# Поиск ресторана по названию, кухни и типа ресторана на главной странице
class Search(ListView):
    template_name = 'main/restaurants.html'
    context_object_name = 'restaurants'
    paginate_by = 6
    filterset_class = RestaurantFilter

    def get_queryset(self):
        query = self.request.GET.get('q')

        if query:
            return Restaurant.objects.filter(Q(name__iregex=query) |
                                             Q(type__name__iregex=query) |
                                             Q(kitchens__name__iregex=query)).distinct()
        else:
            return Restaurant.objects.all()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['q'] = self.request.GET.get('q')

        all_restaurants = context['restaurants']
        current_day_of_week = datetime.now().strftime('%A').lower()

        for restaurant in all_restaurants:
            work_time = WorkTime.objects.get(restaurant=restaurant)

            if work_time:
                opening_time_attr = f'{current_day_of_week}_opening_time'
                closing_time_attr = f'{current_day_of_week}_closing_time'

                restaurant.opening_time = getattr(work_time, opening_time_attr, None)
                restaurant.closing_time = getattr(work_time, closing_time_attr, None)

            reviews = Review.objects.filter(restaurant=restaurant)
            average_rating = reviews.aggregate(models.Avg('rating'))['rating__avg']
            restaurant.average_rating = average_rating

        context['restaurants'] = all_restaurants
        context['filter'] = self.filterset_class(self.request.GET, queryset=self.get_queryset())

        return context


# Поиск публикаций по названию публикации на странице "Публикации"
class SearchPub(ListView):
    template_name = 'main/publications.html'
    context_object_name = 'publications'
    paginate_by = 6

    def get_queryset(self):
        query = self.request.GET.get('q')

        if query:
            return Publication.objects.filter(title__iregex=query)
        else:
            return Publication.objects.all()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['q'] = self.request.GET.get('q')

        return context


# Страница "Публикации"
class PublicationListView(ListView):
    model = Publication
    template_name = 'main/publications.html'
    context_object_name = 'publications'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        return context


# Страница "О нас"
def about(request):
    return render(request, 'main/about.html')


# Профиль пользователя
@login_required
def profile(request):
    if request.method == 'POST':
        form = ProfileEditForm(request.POST, instance=request.user)
        avatar_form = AvatarUploadForm(request.POST, request.FILES, instance=request.user)

        if 'avatar' in request.FILES and avatar_form.is_valid():
            avatar_form.save()
            return redirect('profile')

        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileEditForm(instance=request.user)
        avatar_form = AvatarUploadForm()

    reservations = Reservation.objects.filter(user=request.user).order_by('-date')

    return render(request, 'registration/profile.html', {'form': form,
                                                         'avatar_form': avatar_form,
                                                         'reservations': reservations})


# Страница "Регистрация"
class SignUpView(SuccessMessageMixin, CreateView):
    form_class = CustomUserCreationForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('profile')
    success_message = "Регистрация прошла успешно. Теперь вы вошли в систему."

    def form_valid(self, form):
        # Устанавливаем username равным email перед сохранением формы
        form.instance.username = form.cleaned_data['email']

        response = super().form_valid(form)

        # Вход пользователя после успешной регистрации
        login(self.request, self.object)
        print(f"Пользователь {self.object} только что авторизовался.")

        return response


# Страница "Авторизация"
class UserLoginView(SuccessMessageMixin, LoginView):
    form_class = CustomUserLoginForm
    template_name = 'registration/login.html'
    success_message = 'Успешная авторизация'

    def form_valid(self, form):
        response = super().form_valid(form)
        return response
