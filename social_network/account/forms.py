from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class UserRegistrationForm(forms.Form):
    user_name = forms.CharField(widget=forms.TimeInput(attrs={'class': 'form-control'}))
    user_email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    user_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    user_re_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    def clean_user_email(self):
        user_email = self.data['user_email']
        if User.objects.filter(email=user_email).exists():
            raise ValidationError('this email already exists')
        return user_email

    def clean_user_name(self):
        user_name = self.data['user_name']
        if User.objects.filter(username=user_name).exists():
            raise ValidationError('this username already exists')
        return user_name

    def clean(self):
        form_data = super().clean()
        user_password = form_data.get('user_password')
        user_re_password = form_data.get('user_re_password')
        if user_password and user_re_password and user_password != user_re_password:
            raise ValidationError("password must match")


class UserLoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
