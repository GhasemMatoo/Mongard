from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.text import slugify
from django.contrib import messages
from .models import Post
from .forms import PostForm
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
        post = get_object_or_404(Post, pk=post_id, slug=post_slug)
        return render(request, template_name=self.template_name, context={"posts": post})


class PostDeleteView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        post_id = kwargs.get("post_id")
        post = get_object_or_404(Post, pk=post_id)
        if post.user_id != request.user.id:
            messages.error(request=request, message="you cant delete this post", extra_tags="danger")
        post.delete()
        messages.success(request=request, message="post delete successfully", extra_tags="success")
        return redirect('home:home')


class PostUpdateView(LoginRequiredMixin, View):
    template_name = 'home/update.html'
    form_class = PostForm
    post_id = None
    post_instance = None

    @staticmethod
    def get_post(post_id):
        post = get_object_or_404(Post, pk=post_id)
        return post

    def setup(self, request, *args, **kwargs):
        self.post_id = kwargs.get("post_id")
        self.post_instance = self.get_post(self.post_id)
        return super().setup(request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        if self.post_instance.user_id != request.user.id:
            messages.error(request=request, message=" you cant update is post", extra_tags='danger')
            return redirect('home:home')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return render(request=request, template_name=self.template_name,
                      context={'form': self.form_class(instance=self.get_post(self.post_id))})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, instance=self.post_instance)
        if form.is_valid():
            update_post = form.save(commit=False)
            update_post.slug = slugify(form.cleaned_data['body'][:30])
            update_post.save()
            messages.success(request=request, message="you updated this post", extra_tags="success")
            return redirect('home:post_detail', self.post_id, self.post_instance.slug)


class PostCreateView(LoginRequiredMixin, View):
    template_name = 'home/create.html'
    form_class = PostForm

    def get(self, request, *args, **kwargs):
        return render(request=request, template_name=self.template_name, context={"form": self.form_class})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.slug = slugify(form.cleaned_data['body'][:30])
            new_post.user = request.user
            new_post.save()
            messages.success(request=request, message="you created a new post", extra_tags="success")
            return redirect('home:post_detail', new_post.id, new_post.slug)
