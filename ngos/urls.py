from django.urls import path
from . import views
from .views import recommend_ngos,ngo_details

urlpatterns = [
    path('login/', views.login_ngo, name='login_ngo'),
    path('logout/', views.logout_ngo, name='logout_ngo'),
    path('update/', views.update_ngo, name='update_ngo'),
    path('register/', views.register_ngo, name='register_ngo'),
    path('profile/', views.view_ngo, name='view_ngo'),
    path('recommend-ngos/', recommend_ngos, name='recommend-ngos'),
    path('ngo-detail/<int:ngo_id>/', ngo_details, name='ngo-details'),
    path('email/', views.email_service, name='email_service')
]
