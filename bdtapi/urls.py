from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from authentication.urls import urlpatterns as authentication_urls

from orders.views import OrderViewSet


router = routers.SimpleRouter()
router.register(r'orders', OrderViewSet, 'orders')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v0/', include(router.urls)),
] + authentication_urls
