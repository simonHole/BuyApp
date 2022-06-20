from django.http import HttpResponse
from django.urls import path
from django.http import HttpResponse
from . import views

# Create your URL's here
urlpatterns = [
    path('project/<str:pk>/', views.project, name='project'),
    path('', views.projects, name='projects'),
    path('create-project/', views.create_project, name='create-project'),
    path('update-project/<str:pk>/', views.update_project, name='update-project'),
    path('delete-project/<str:pk>/', views.delete_project, name='delete-project'),
]
