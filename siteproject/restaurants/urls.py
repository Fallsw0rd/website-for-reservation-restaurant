from django.urls import path
from . import views


app_name = 'restaurants'

urlpatterns = [
    path('create/', views.create_restaurant, name='create'),
    path('<str:name>/<int:pk>', views.RestaurantDetailView.as_view(), name='profile-rest'),
    path('<str:name>/<int:pk>/update/', views.RestaurantUpdateView.as_view(), name='update'),
    path('check_reservation/', views.check_reservation, name='check_reservation'),
    path('<str:name>/<int:pk>/tables/', views.ReservationCreateView.as_view(), name='reservation'),
    path('<str:name>/<int:pk>/review/', views.create_review, name='review'),
    path('<str:name>/<int:pk>/reservations/', views.reservations_tables, name='reservations'),
    path('confirm_reservation/<int:reservation_id>/', views.confirm_reservation, name='confirm_reservation'),
    path('cancel_reservation/<int:reservation_id>/', views.cancel_reservation, name='cancel_reservation'),
    path('get_time_choices/', views.get_time_choices, name='get_time_choices'),
]
