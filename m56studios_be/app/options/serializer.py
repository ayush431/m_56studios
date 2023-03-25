from rest_framework import serializers
from .model import options

class OptionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = options
        fields = "__all__"
