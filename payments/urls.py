from django.urls import path
from .views import initiate_payment

urlpatterns = [
    path('pay/', initiate_payment, name='initiate_payment'),
]
