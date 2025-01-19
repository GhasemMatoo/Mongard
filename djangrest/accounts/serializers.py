from rest_framework import serializers


def clean_email(email: str) -> str:
    if 'admin' in email:
        raise serializers.ValidationError('admin cant be in email')


class UserRegisterSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    email = serializers.EmailField(required=True, validators=[clean_email])
    password = serializers.CharField(required=True, write_only=True)
    password2 = serializers.CharField(required=True, write_only=True)

    def validate_username(self, username):
        if username == 'admin':
            raise serializers.ValidationError('username cant be `admin`')
        return username

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError('password must match')
        return data
