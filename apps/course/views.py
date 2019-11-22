from django.db import transaction
from django.shortcuts import render
from django.views.decorators.cache import cache_page
from rest_framework import viewsets, status, permissions, mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework_extensions.cache.mixins import CacheResponseMixin

from apps.course.models import Course, CourseImage, Questions, QuestionsAnswer
from apps.course.serializers import CourseDetailSerializers, QuestionCreateSerializers, QuestionSampleSerializers, \
    QuestionAnswerCreateSerializers, QuestionAnswerSerializers, CourseSampleSerializers
from django_filters.rest_framework import DjangoFilterBackend
from utils.pagination import SmallResultsSetPagination


class CourseViewSet(CacheResponseMixin, viewsets.ModelViewSet):
    filter_backends = (DjangoFilterBackend,)
    permission_classes = (IsAuthenticated,)
    filter_fields = ('is_active',)
    pagination_class = SmallResultsSetPagination

    def get_queryset(self):
        """
        根据人员身份不同返回不同的课程列表
        :return:
        """
        try:
            if self.request.user.is_teacher or self.request.user.is_staff or self.request.user.is_superuser:
                return Course.objects.all().filter(is_active=True).order_by("id")
            else:
                return Course.objects.all().filter(is_active=True).order_by("id")
        except AttributeError as e:
            return Course.objects.all().filter(is_active=True).order_by("id")

    def perform_create(self, serializer):
        with transaction.atomic():
            serializer.save(create_user=self.request.user)

    def get_serializer_class(self):
        if self.action == 'list':
            return CourseSampleSerializers
        return CourseDetailSerializers


class QuestionViewSet(viewsets.ModelViewSet):
    pagination_class = SmallResultsSetPagination
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('question_type', 'course_id',)
    queryset = Questions.objects.all().order_by("show_time")

    def get_serializer_class(self):
        if self.action == 'create':
            return QuestionCreateSerializers
        if self.action == 'list' or self.action == 'retrieve':
            return QuestionSampleSerializers
        return QuestionSampleSerializers

    def perform_create(self, serializer):
        with transaction.atomic():
            serializer.save(create_user=self.request.user)


class QuestionAnswerViewSet(viewsets.ModelViewSet):
    pagination_class = SmallResultsSetPagination
    permission_classes = (IsAuthenticated,)
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('questions', 'is_right',)
    queryset = QuestionsAnswer.objects.all().order_by("create_time")

    def get_serializer_class(self):
        if self.action == 'create':
            return QuestionAnswerCreateSerializers
        return QuestionAnswerSerializers

    def perform_create(self, serializer):
        with transaction.atomic():
            serializer.save(user=self.request.user)
