from django.urls import path, include

from rest_framework.routers import DefaultRouter

from area.views import StoreAreaViewSet


router = DefaultRouter()
router.register(r'', StoreAreaViewSet, base_name='area')


urlpatterns = [
    path('', include(router.urls))
]
