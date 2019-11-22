from django.urls import path, include

from rest_framework.routers import DefaultRouter

from apps.course.views import CourseViewSet,QuestionViewSet,QuestionAnswerViewSet


router = DefaultRouter()
router.register(r'course', CourseViewSet, base_name='course')
router.register(r'question', QuestionViewSet, base_name='course')
router.register(r'answer', QuestionAnswerViewSet, base_name='course')


urlpatterns = [
    path('', include(router.urls))
]
