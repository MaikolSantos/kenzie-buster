from rest_framework import serializers
from .models import User


class UserSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    email = serializers.EmailField(max_length=127, unique=True)
    first_name = serializers.CharField(max_length=50)
    last_name = serializers.CharField(max_length=50)
    birthdate = serializers.DateField(allow_null=True)
    password = serializers.CharField(max_length=127, write_only=True)
    is_employee = serializers.BooleanField(allow_null=True, default=False)

    def create(self, validated_data):
        if validated_data["is_employee"]:
            return User.objects.create_user(
                **validated_data, is_employee=True, is_superuser=True
            )
        else:
            return User.objects.create_user(
                **validated_data, is_employee=False, is_superuser=False
            )
