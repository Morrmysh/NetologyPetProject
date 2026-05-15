from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from dj_rest_auth.serializers import PasswordResetSerializer
from django.db import transaction

from shop.models import Product, ParameterValue, Parameter

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


class OwnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']


class ParameterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parameter
        fields = ['id', 'name']

class ParameterValueSerializer(serializers.ModelSerializer):
    parameter_name = serializers.CharField(write_only=True)
    parameter = ParameterSerializer(read_only=True)

    class Meta:
        model = ParameterValue
        fields = ['id', 'parameter', 'parameter_name', 'value']

    def create(self, validated_data):
        name = validated_data.pop('parameter_name')
        parameter, _ = Parameter.objects.get_or_create(name=name)
        return ParameterValue.objects.create(parameter=parameter, **validated_data)


class ProductSerializer(serializers.ModelSerializer):
    owner = OwnerSerializer(read_only=True)
    parameter_values = ParameterValueSerializer(many=True)

    class Meta:
        model = Product
        fields = ['id', 'name', 'comment', 'price', 'available', 'owner', 'parameter_values']
        extra_kwargs = {
            'name': {'required': True}
        }

    def create(self, validated_data):
        with transaction.atomic():
            product_parameter_data = validated_data.pop('parameter_values', [])
            product = Product.objects.create(**validated_data)

            for parameter_data in product_parameter_data:
                name = parameter_data.pop('parameter_name')
                parameter, _ = Parameter.objects.get_or_create(name=name)
                ParameterValue.objects.create(
                    product=product,
                    parameter=parameter,
                    **parameter_data
                )
            return product