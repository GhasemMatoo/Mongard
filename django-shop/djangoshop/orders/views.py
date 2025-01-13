from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from home.models import Product
from .cart import Cart
from .forms import CartAddForm

# Create your views here.


class CartView(View):
    template_name = 'orders/cart.html'

    def get(self, request, *args, **kwargs):
        cart = Cart(request)
        return render(request=request, template_name=self.template_name, context={"cart": cart})


class CartAddView(View):
    form_class = CartAddForm

    def post(self, request, *args, **kwargs):
        product_id = kwargs.get("product_id")
        cart = Cart(request)
        product = get_object_or_404(Product, id=product_id)
        form = CartAddForm(request.POST)
        if form.is_valid():
            cart.add(product, form.cleaned_data['quantity'])
        return redirect("orders:cart")


class CartRemoveView(View):
    def get(self, request, *args, **kwargs):
        cart = Cart(request)
        product = get_object_or_404(Product, id=kwargs.get("product_id"))
        cart.delete(product.id)
        return redirect("orders:cart")
