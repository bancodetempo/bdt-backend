from rest_framework import routers
from django.urls import path, include
from authentication.views import AuthenticationViewSet

router = routers.SimpleRouter()
router.register(r'authentication', AuthenticationViewSet, 'authentication')

urlpatterns = router.urls
