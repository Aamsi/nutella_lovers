from django.contrib import admin
from django.urls import path, include

import substitute.views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('substitute/', include('substitute.urls'))
]
