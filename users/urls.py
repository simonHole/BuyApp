from django import views
from django.urls import path
from . import views

urlpatterns = [
    path('', views.profiles, name='profiles'),
    path('profile/<str:pk>/', views.userProfile, name='user-profile'),
    path('login/', views.login_profile, name='login'),
    path('logout/', views.logout_profile, name='logout'),
    path('register/', views.register_profile, name='register-profile'),
    path('account/', views.user_account, name='account'),
    path('edit-account/', views.edit_account, name='edit-account'),
    path('create-technology/', views.create_technology, name='create-technology'),
    path('update-technology/<str:pk>/',
         views.update_technology, name="update-technology"),
    path('delete-technology/<str:pk>',
         views.delete_technology, name='delete-technology'),
]
