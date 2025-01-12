from django.shortcuts import render
from django.views import View

# Create your views here.


class CartView(View):
    template_name = 'orders/card.html'
    def get(self, request, *args, **kwargs):
        return render(request=request, template_name=self.template_name, context={})