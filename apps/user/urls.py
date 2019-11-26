from django.urls import path, include

from rest_framework.routers import DefaultRouter

from user.views import UserViewSet, UserProfileViewSet


router = DefaultRouter()
router.register(r'', UserViewSet, base_name='user')
router.register(r'profile', UserProfileViewSet, base_name='user')


urlpatterns = [
    path('', include(router.urls))
]
