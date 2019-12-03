from django.db import transaction
from django.shortcuts import render

# Create your views here.
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from area.models import StoreArea
from utils.pagination import SmallResultsSetPagination
from area.serializers import StoreAreaSampleSerializers, StoreAreaDetailSerializers


class StoreAreaViewSet(viewsets.ModelViewSet):

    filter_backends = (DjangoFilterBackend,)
    permission_classes = (IsAuthenticated,)
    filter_fields = ('status',)
    pagination_class = SmallResultsSetPagination

    def get_queryset(self):
        """
        根据人员身份不同返回不同的课程列表
        :return:
        """
        try:
            if self.request.user.is_superuser or self.request.user.is_staff:
                return StoreArea.objects.all().order_by("id")
            else:
                return StoreArea.objects.all().filter(active=True).order_by("id")
        except AttributeError as e:
            return StoreArea.objects.all().filter(active=True).order_by("id")

    def perform_create(self, serializer):
        with transaction.atomic():
            serializer.save(creator=self.request.user)

    def get_serializer_class(self):
        if self.action == 'list':
            return StoreAreaSampleSerializers
        return StoreAreaDetailSerializers
