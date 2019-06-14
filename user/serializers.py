from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken


class UserSerializer(serializers.ModelSerializer):
    token = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = get_user_model()
        fields = (
            'email', 'firstname', 'lastname', 'password', 'token'
            )
        extra_kwargs = {
            'password': {'write_only': True, 'min_length': 6},
            }

    def get_token(self, obj):
        refresh = RefreshToken.for_user(obj)

        return f'Bearer {str(refresh.access_token)}'

    def create(self, validated_data):
        user = get_user_model().objects.create_user(**validated_data)
        return user


class UserLoginSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=200, required=True)
    password = serializers.CharField(write_only=True, max_length=200, required=True)
    token = serializers.SerializerMethodField(read_only=True)

    def get_token(self, validated_data):
        user = get_user_model().objects.get(email=validated_data.get('email'))
        refresh = RefreshToken.for_user(user)

        token = f'Bearer {str(refresh.access_token)}'
        return str(token)
