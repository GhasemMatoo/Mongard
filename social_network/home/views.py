from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from .models import Post
# Create your views here.


class HomeView(View):
    template_name = 'home/home.html'

    def get(self, request):
        posts = Post.objects.all()
        return render(request=request, template_name=self.template_name, context={'posts': posts})

    def post(self, request):
        return render(request=request, template_name=self.template_name)


class PostDetailView(LoginRequiredMixin, View):
    template_name = 'home/detail.html'

    def get(self, request, *args, **kwargs):
        post_id = kwargs.get("post_id")
        post_slug = kwargs.get("post_slug")
        post = Post.objects.get(pk=post_id, slug=post_slug)
        return render(request, template_name=self.template_name, context={"posts": post})


class PostDeleteView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        post_id = kwargs.get("post_id")
        post = Post.objects.get(pk=post_id)
        if post.user_id != request.user.id:
            messages.error(request=request, message="you cant delete this post", extra_tags="danger")
        post.delete()
        messages.success(request=request, message="post delete successfully", extra_tags="success")
        return redirect('home:home')
