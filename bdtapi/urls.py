from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from authentication.urls import urlpatterns as authentication_urls

from orders.views import OrderViewSet


router = routers.SimpleRouter()
router.register(r'orders', OrderViewSet, 'orders')

order_urls = router.urls

api_urls = authentication_urls + order_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v0/', include(api_urls)),
]
