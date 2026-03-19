from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),

    path('backup/', views.download_backup, name='download_backup'),

    path('register/', views.register, name='register'),
]