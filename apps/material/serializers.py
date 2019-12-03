# coding=utf-8
from rest_framework import serializers, exceptions
from utils import logger
from material.models import *
from django.core.exceptions import ImproperlyConfigured, PermissionDenied


class MaterialSampleSerializers(serializers.ModelSerializer):

    class Meta:
        model = Material
        fields = '__all__'


class MaterialDetailSerializers(serializers.ModelSerializer):

    class Meta:
        model = Material
        fields = "__all__"
