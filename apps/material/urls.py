from django.urls import path, include

from rest_framework.routers import DefaultRouter

from material.views import MaterialViewSet


router = DefaultRouter()
router.register(r'', MaterialViewSet, base_name='material')


urlpatterns = [
    path('', include(router.urls))
]
