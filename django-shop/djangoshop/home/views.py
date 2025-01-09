from django.shortcuts import render, get_object_or_404
from django.views import View
from .models import Product
# Create your views here.


class HomeView(View):
    template_name = 'home/home.html'

    def get(self, request):
        products = Product.objects.all()
        return render(request=request, template_name=self.template_name, context={"products": products})


class ProductDetailView(View):
    template_name = 'home/detail.html'

    def get(self, request, *args, **kwargs):
        slug = self.kwargs['slug']
        product = get_object_or_404(Product, slug=slug)
        return render(request=request, template_name=self.template_name, context={'product': product})
