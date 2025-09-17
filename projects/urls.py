from django.urls import path
from . import views

urlpatterns = [
    path('update/<int:project_id>/', views.update_project, name='update_project'),
    path('create/', views.create_project, name='create_project'),
    path('details/<int:project_id>/', views.view_details, name='view_details'),
    path('list/<int:ngo_id>/', views.list_projects, name='list_projects'),
]
