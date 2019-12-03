# coding=utf-8
from rest_framework import serializers, exceptions
from utils import logger
from location.models import *
from django.core.exceptions import ImproperlyConfigured, PermissionDenied


class StoreLocationSampleSerializers(serializers.ModelSerializer):

    class Meta:
        model = StoreLocation
        fields = ('id', 'location_name', 'location_code', 'location_type', 'status', 'store_count', 'store_count', )


class StoreLocationDetailSerializers(serializers.ModelSerializer):

    class Meta:
        model = StoreLocation
        fields = "__all__"
