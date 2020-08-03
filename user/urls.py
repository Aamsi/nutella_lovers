from django.contrib import admin
from django.urls import path, include

from . import views

urlpatterns = [
    path('signup/', views.signup, name='create_account'),
    path('logout/', views.signout, name='signout'),
    path('login/', views.signin, name='signin'),
    path('myaccount/', views.my_account, name='myaccount')
]