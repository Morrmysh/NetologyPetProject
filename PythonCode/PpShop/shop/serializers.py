from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from dj_rest_auth.serializers import PasswordResetSerializer

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    token = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'token']

    def get_token(self, user):
        token, _ = Token.objects.get_or_create(user=user)
        return token.key

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password']
        )
        Token.objects.get_or_create(user=user)
        return user


class CustomPasswordResetSerializer(PasswordResetSerializer):
    def validate_email(self, value):
        try:
            validate_email(value)
            data = {'email__iexact': value}
        except ValidationError:
            data = {'username': value}

        try:
            user = User.objects.get(**data)
        except User.DoesNotExist:
            return ''

        return user.email
