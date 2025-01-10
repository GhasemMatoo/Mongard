from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.contrib import messages
from .models import Product
from . import tasks
from .forms import UploadFile
from bucket import bucket
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


class BucketHomeView(View):
    template_name = 'home/bucket.html'

    def get(self, request, *args, **kwargs):
        objects = tasks.all_bucket_objects_task()
        return render(request=request, template_name=self.template_name, context={"objects": objects})


class DeleteBucketObjectView(View):
    def get(self, request, *args, **kwargs):
        key = kwargs.get('key')
        tasks.delete_object_task(key=key)
        messages.success(request=request, message='yor object will be delete soon', extra_tags='info')
        return redirect('home:bucket')


class DownloadBucketObjectView(View):
    def get(self, request, *args, **kwargs):
        key = kwargs.get("key")
        tasks.download_object_task(key=key)
        messages.success(request=request, message='yor download object will start soon', extra_tags='info')
        return redirect('home:bucket')


class UploadBuketObjectView(View):
    template_name = 'home/upload.html'
    form_class = UploadFile

    def get(self, request, *args, **kwargs):
        return render(request=request, template_name=self.template_name, context={'form': self.form_class})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            bucket.upload_object(request.FILES["file"])
            messages.success(request=request, message='yor uploads images will soon', extra_tags='success')
            return redirect('home:bucketUpload')
        messages.error(request=request, message='yor can upload images', extra_tags='danger')
