# coding=utf-8


from rest_framework import serializers, exceptions
from utils import logger
from area.models import *
from django.core.exceptions import ImproperlyConfigured, PermissionDenied


class StoreAreaSampleSerializers(serializers.ModelSerializer):

    class Meta:
        model = StoreArea
        fields = ('id', 'area_name', 'area_code', 'area_type', 'status', 'created_at',)


class StoreAreaDetailSerializers(serializers.ModelSerializer):

    class Meta:
        model = StoreArea
        fields = "__all__"
