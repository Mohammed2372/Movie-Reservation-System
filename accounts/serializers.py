from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from django.contrib.auth.models import User


class RegisterSerializer(ModelSerializer):
    password = serializers.CharField(
        write_only=True, required=True, style={"input_type": "password"}
    )
    password2 = serializers.CharField(
        write_only=True,
        required=True,
        style={"input_type": "password"},
        label="Confirm Password",
    )

    class Meta:
        model = User
        fields = ["username", "email", "password", "password2"]

    def validate(self, data):
        # Check if passwords match
        if data["password"] != data["password2"]:
            raise serializers.ValidationError({"password": "Passwords do not match."})

        # Check if email is unique
        if User.objects.filter(email=data.get("email")).exists():
            raise serializers.ValidationError({"email": "Email already registered."})

        return data

    def create(self, validated_data):
        validated_data.pop("password2")

        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"],
        )
        return user


# --- Login --- #
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()


# --- User Detail --- #
class UserDetailSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email"]
