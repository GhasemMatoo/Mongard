from django.shortcuts import render
from django.views import View
from .forms import UserRegistrationForm
# Create your views here.


class RegisterView(View):
    template_name = 'account/register.html'
    form_class = UserRegistrationForm

    def get(self, request):
        return render(request=request, template_name=self.template_name, context={"form": self.form_class})

    def post(self, request):
        return render(request=request, template_name=self.template_name)
