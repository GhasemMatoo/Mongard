from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Writer
from .forms import UserRegistrationForm


# Create your views here.


class Home(View):
    template_name = 'home/home.html'

    def get(self, request):
        return render(request=request, template_name=self.template_name)


class About(View):
    template_name = "home/home.html"

    def get(self, request):
        return render(request=request, template_name=self.template_name)


class UserRegisterView(View):
    template_name = 'home/register.html'
    form_class = UserRegistrationForm

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home:home')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        return render(request=request, template_name=self.template_name, context={"form": self.form_class()})

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


class WriterView(LoginRequiredMixin, View):
    template_name = 'home/register.html'

    def get(self, request):
        writers = Writer.objects.all()
        return render(request=request, template_name=self.template_name, context={"writers": writers})
