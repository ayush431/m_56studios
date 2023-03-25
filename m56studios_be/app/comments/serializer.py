from rest_framework import serializers
from .model import comments

class CommentsSerialiser(serializers.ModelSerializer):
    class Meta:
        model = comments
        fields = ["cmt_id", "comment", "created_at", "user_details", "qus", "user"]
