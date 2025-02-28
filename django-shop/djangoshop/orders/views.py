from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib import messages
from django.views import View
from home.models import Product
from .cart import Cart
from .forms import CartAddForm, CouponApplyForm
from .models import Order, OrderItem, Coupon
import datetime


# Create your views here.


class CartView(View):
    template_name = 'orders/cart.html'

    def get(self, request, *args, **kwargs):
        cart = Cart(request)
        return render(request=request, template_name=self.template_name, context={"cart": cart})


class CartAddView(PermissionRequiredMixin, View):
    form_class = CartAddForm
    permission_required = 'orders.ad_order'

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


class OrdersCreateView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        cart = Cart(request)
        order = Order.objects.create(user=request.user)
        for item in cart:
            OrderItem.objects.create(
                order=order, product=item['product'], price=item['price'], quantity=item['quantity'])
            cart.clear()
        return redirect('orders:orders_detail', order.id)


class OrdersDetailView(LoginRequiredMixin, View):
    template_name = 'orders/order.html'
    form_class = CouponApplyForm

    def get(self, request, *args, **kwargs):
        order_id = kwargs.get("order_id")
        order = get_object_or_404(Order, id=order_id)
        context_data = {'order': order, 'form': self.form_class}
        return render(request=request, template_name=self.template_name, context=context_data)


class CouponApplyView(LoginRequiredMixin, View):
    form_class = CouponApplyForm

    def post(self, rquest, *args, **kwargs):
        now = datetime.datetime.now()
        form = self.form_class(rquest.POST)
        if form.is_valid():
            order_id = kwargs['order_id']
            code = form.cleaned_data['code']
            try:
                coupon = Coupon.objects.get(code__exact=code, valid_from__lt=now, valid_to__gte=now, active=True)
            except Coupon.DoesNotExist:
                messages.error(request=rquest, message="this coupon does not exists", extra_tags='danger')
                return redirect('orders:orders_detail')

            order = Order.objects.get(id=order_id)
            order.discount = coupon.discount
            order.save()
            return redirect('orders:orders_detail', order_id)
