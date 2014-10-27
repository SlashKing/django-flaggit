import re

from rest_framework import serializers
from rest_framework.reverse import reverse_lazy

from .models import *


class ReasonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reason


class FlagSerializer(serializers.Serializer):
    app_model = serializers.CharField(max_length=50)
    object_id = serializers.IntegerField()

    comment = serializers.CharField(max_length=300, required=False)
    reason_id = serializers.IntegerField(required=False)

    def validate_app_model(self, attrs, source):
        """ check format as 'appname.modelname' """
        value = attrs[source]
        if not re.match(r'^\w+\.\w+$', value):

            raise serializers.ValidationError("wrong format, use 'appname.modelname' ")
        return attrs

    def validate(self, attrs):
        if attrs.get('comment') or attrs.get('reason_id') :
            return attrs
        raise serializers.ValidationError("need to define either reason or comment")

