from django.shortcuts import render, redirect
from django.views import View
from .forms import UserRegistrationForm, UserLoginForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import views as auth_views
# Create your views here.


class RegisterView(View):
    template_name = 'account/register.html'
    form_class = UserRegistrationForm

    def get(self, request):
        return render(request=request, template_name=self.template_name, context={"form": self.form_class})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            user_form_data = form.cleaned_data
            User.objects.create_user(username=user_form_data["user_name"],
                                     email=user_form_data["user_email"],
                                     password=user_form_data["user_password"]
                                     )
            messages.success(request=request, message="you registered successfully", extra_tags="success")
            return redirect('home:home')
        messages.error(request=request, message="you Input data not valid", extra_tags="error")
        return render(request=request, template_name=self.template_name, context={"form": self.form_class})


class UserLoginView(View):
    template_name = 'account/login.html'
    form_class = UserLoginForm

    def get(self, request):
        return render(request=request, template_name=self.template_name, context={"form": self.form_class})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            form_data = form.cleaned_data
            username = form_data.get("username")
            password = form_data.get("password")
            user = authenticate(request=request, username=username, password=password)
            if user is not None:
                login(request=request, user=user)
                messages.success(request=request, message='you logged in successfully', extra_tags="success")
                return redirect('home:home')
        messages.warning(request=request, message='username or password is wrong', extra_tags='warning')
        return render(request=request, template_name=self.template_name, context={"form": self.form_class})


class UserLogoutView(View):
    @staticmethod
    def get(request):
        logout(request=request)
        messages.success(request=request, message='you logout successfully', extra_tags='success')
        return redirect('home:home')
