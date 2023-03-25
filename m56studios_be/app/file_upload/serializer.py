from rest_framework import serializers
from django.core.validators import FileExtensionValidator

class UploadSerializer(serializers.Serializer):
    file = serializers.FileField(validators=[FileExtensionValidator(allowed_extensions=['xlsx'])])