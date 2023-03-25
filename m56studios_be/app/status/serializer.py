from rest_framework import serializers
from .model import status_log

class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = status_log
        fields = ['id', 'old_status', 'new_status', 'created_at', 'qn_id', 'user_id', 'qn_with_tagged_images']