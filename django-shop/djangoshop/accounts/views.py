import random

from django.shortcuts import render, redirect
from django.views import View
from .forms import UserRegisterForm, VerifyCodeForm
from utils import send_otp_code
from .models import User, OtpCode
from django.contrib import messages
# Create your views here.


class UserRegisterView(View):
    template_name = 'accounts/register.html'
    form_class = UserRegisterForm

    def get(self, request):
        return render(request=request, template_name=self.template_name, context={"form": self.form_class})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            phone_number = form.cleaned_data["phone"]
            random_code = random.randint(1000, 9999)
            if not send_otp_code(phone_number, random_code):
                messages.error(request=request, message='not send sms ', extra_tags='danger')
                return redirect('account:register')
            OtpCode.objects.create(phone_number=phone_number, code=random_code)
            request.session["user_registeration_info"] = form.cleaned_data
            messages.success(request=request, message='we sent you a code', extra_tags='success')
            return redirect('account:verify_code')
        return render(request=request, template_name=self.template_name, context={'form': form})


class UserRegisterVerifyCodeView(View):
    template_name = 'accounts/verify.html'
    form_class = VerifyCodeForm

    def get(self, request):
        return render(request=request, template_name=self.template_name, context={'form': self.form_class})

    def post(self, request):
        user_session = request.session["user_registeration_info"]
        code_instance = OtpCode.objects.get(phone_number=user_session['phone'])
        form = VerifyCodeForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            if cd['code'] == code_instance.code:
                User.objects.create_user(
                    phone_number=user_session['phone'],
                    email=user_session['email'],
                    full_name=user_session['full_name'],
                    password=user_session['password']
                )
                code_instance.delete()
                messages.success(request=request, message='yor registered.', extra_tags='success')
                return redirect('home:home')
            else:
                messages.error(request=request, message='this code is wrong', extra_tags='danger')
                return redirect('account:verify_code')
        return render(request=request, template_name=self.template_name, context={'form': form})


