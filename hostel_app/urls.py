from django.urls import path
from . import views

urlpatterns = [
    path('', views.main_page, name='main_page'),
    path('index/', views.main_page, name='main_page'),
    path('rooms/', views.room_list, name='room_list')
]