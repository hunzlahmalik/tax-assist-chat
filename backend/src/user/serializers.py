from typing import Any, Callable

from django.contrib.auth.hashers import make_password
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ("user_permissions", "groups")
        create_only_fields = ["username", "email"]
        extra_kwargs = {
            "username": {"required": False, "allow_blank": False},
            "email": {"required": False, "allow_blank": False},
            "password": {
                "required": False,
                "write_only": True,
                "validators": [validate_password],
                "min_length": 8,
                "max_length": 128,
                "style": {"input_type": "password"},
                "error_messages": {
                    "blank": "This field may not be blank.",
                    "required": "This field is required.",
                },
            },
            "id": {"read_only": True},
            "is_staff": {"read_only": True},
            "is_active": {"read_only": True},
            "is_superuser": {"read_only": True},
            "date_joined": {"read_only": True},
            "last_login": {"read_only": True},
            "user_permissions": {"read_only": True},
        }

    @staticmethod
    def validate_password(password):
        return make_password(password)

    @staticmethod
    def validate_fields(
        fields: list,
        data: dict[str, Any],
        condition: Callable[[str, dict], bool],
        message: str,
    ) -> dict[str, list[str]]:
        return {field: [message] for field in fields if not condition(field, data)}

    def create(self, validated_data):
        errors = UserSerializer.validate_fields(
            [*self.Meta.create_only_fields, "password"],
            validated_data,
            lambda f, d: f in validated_data,
            "This field is required.",
        )
        if bool(errors):
            raise serializers.ValidationError(errors)
        return super().create(validated_data)

    def update(self, instance, validated_data):
        errors = {
            field: ["It is not allowed to change this field."]
            for field in self.Meta.create_only_fields
            if field in validated_data and validated_data[field] != getattr(instance, field)
        }
        if bool(errors):
            raise serializers.ValidationError(errors)
        return super().update(instance, validated_data)


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token["username"] = user.username

        return token
