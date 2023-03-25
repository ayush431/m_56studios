from rest_framework import serializers
from ..models import user_model


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = user_model
        fields = ['user_id', 'first_name', 'last_name',
                  'email', 'password', "is_active", "user_type"]
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)

        instance.save()
        return instance

class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = user_model
        fields = ['user_id', 'first_name', 'last_name',
                  'email', "is_active", "user_type"]