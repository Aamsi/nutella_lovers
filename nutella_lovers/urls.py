from django.contrib import admin
from django.urls import path, include

from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='welcome'),
    path('account/', include('user.urls')),
    path('substitute/', include('substitute.urls')),
]
