from django.urls import path

from . import views

app_name = 'matching'

urlpatterns = [
    path('', views.index, name='index'),
    path('api/search/', views.search_mentors, name='search_mentors'),
]
