from django.contrib import admin
from django.urls import path, include

from . import views

urlpatterns = [
    path('search/', views.search_substitute, name='search'),
    path('save/', views.save_substitute, name='save'),
]