from django.contrib.auth.views import LogoutView
from django.urls import path
from . import views
from .views import SignUpView, UserLoginView

urlpatterns = [
    path('', views.index, name='main'),
    path('restaurants/', views.RestaurantListView.as_view(), name='restaurants'),
    path('restaurants/search/', views.Search.as_view(), name='search'),
    path('about', views.about, name='about'),
    path('publications/', views.PublicationListView.as_view(), name='publications'),
    path('publications/search/', views.SearchPub.as_view(), name='search_pub'),
    path('profile/', views.profile, name='profile'),
    path('registration/', SignUpView.as_view(), name='registrations'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]
