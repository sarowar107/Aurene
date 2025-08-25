# aurene_backend/urls.py

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('shop_api.urls')),
    path('payment/', include('payment.urls')),
]