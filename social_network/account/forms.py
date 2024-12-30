from django import forms


class UserRegistrationForm(forms.Form):
    user_name = forms.CharField()
    user_email = forms.EmailField()
    user_password = forms.CharField()
