from django.urls import path
from . import views

urlpatterns = [
    path('show_form/', views.show_form, name='show_form'),
    path('user_donations/', views.list_user_donations, name='list_user_donations'),
    path('ngo_donations/', views.list_ngo_donations, name='list_ngo_donations'),
]
