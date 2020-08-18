from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from authentication.urls import urlpatterns as authentication_urls
from orders.urls import urlpatterns as order_urls


api_urls = authentication_urls + order_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v0/', include(api_urls)),
]
