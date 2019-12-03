from django.urls import path, include

from rest_framework.routers import DefaultRouter

from location.views import StoreLocationViewSet


router = DefaultRouter()
router.register(r'', StoreLocationViewSet, base_name='location')


urlpatterns = [
    path('', include(router.urls))
]
