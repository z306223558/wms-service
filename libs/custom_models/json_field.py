# coding=utf-8
from django.db import models
import json


class JSONField(models.TextField):

    description = "Json"

    def to_python(self, value):
        v = models.TextField.to_python(self, value)
        try:
            return json.loads(v)
        except json.JSONDecodeError as e:
            pass
        return v

    def get_prep_value(self, value):
        return json.dumps(value)
