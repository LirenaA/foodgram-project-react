from users.models import CustomUser, Follow
from recipes.models import Recipe
from rest_framework import serializers, status, validators
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from rest_framework.validators import ValidationError


User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор регистрации/получения информации пользователя."""
    
    def create(self, validated_data):
        user = CustomUser(
            email=validated_data['email'],
            username=validated_data['username'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
    

    class Meta:
        model = CustomUser
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'password',
        )
        extra_kwargs = {
            'password': {'write_only': True},
        }

class PasswordSerializer(serializers.Serializer):
    """Сериализатор смены пароля."""
    new_password = serializers.CharField(max_length=150)
    current_password = serializers.CharField(max_length=150)

    def validate(self, value):
        if value['new_password'] == value['current_password']:
            raise serializers.ValidationError(
                {'status': 'Поля не должны совпадать'})
        return value
    

