from rest_framework import serializers
from django.contrib.auth.models import User


def clean_email(email: str) -> str:
    if 'admin' in email:
        raise serializers.ValidationError('admin cant be in email')


class UserRegisterSerializer(serializers.ModelSerializer):
    # username = serializers.CharField(required=True)
    # email = serializers.EmailField(required=True, validators=[clean_email])
    # password = serializers.CharField(required=True, write_only=True)
    password2 = serializers.CharField(required=True, write_only=True)
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2']
        extra_kwargs = {
            'password': {'write_only': True},
            'email': {'validators': (clean_email,)}
        }

    def create(self, validated_data):
        del validated_data['password2']
        return User.objects.create_user(**validated_data)

    def validate_username(self, username):
        if username == 'admin':
            raise serializers.ValidationError('username cant be `admin`')
        return username

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError('password must match')
        return data


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
