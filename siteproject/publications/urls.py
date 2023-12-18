from django.urls import path
from . import views

app_name = 'publications'

urlpatterns = [
    path('<int:pk>', views.PublicationDetailView.as_view(), name='publication'),
]
