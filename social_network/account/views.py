from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from .forms import UserRegistrationForm, UserLoginForm, EditUserForm
from .models import Relation


# Create your views here.


class RegisterView(View):
    template_name = 'account/register.html'
    form_class = UserRegistrationForm

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home:home')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        return render(request=request, template_name=self.template_name, context={"form": self.form_class})

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


class UserLoginView(View):
    template_name = 'account/login.html'
    form_class = UserLoginForm
    next = None

    def setup(self, request, *args, **kwargs):
        self.next = request.GET.get('next')
        return super().setup(request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home:home')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        return render(request=request, template_name=self.template_name, context={"form": self.form_class})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            form_data = form.cleaned_data
            username = form_data.get("username")
            password = form_data.get("password")
            user = authenticate(request=request, username=username, password=password)
            if user is not None:
                login(request=request, user=user)
                messages.success(request=request, message='you logged in successfully', extra_tags="success")
                if self.next:
                    return redirect(self.next)
                return redirect('home:home')
        messages.warning(request=request, message='username or password is wrong', extra_tags='warning')
        return render(request=request, template_name=self.template_name, context={"form": self.form_class})


class UserLogoutView(View):
    @staticmethod
    def get(request):
        logout(request=request)
        messages.success(request=request, message='you logout successfully', extra_tags='success')
        return redirect('home:home')


class UserProfileView(LoginRequiredMixin, View):
    template_name = 'account/profile.html'

    def get(self, request, *args, **kwargs):
        is_following = False
        user_id = kwargs.get("user_id")
        user = get_object_or_404(User, pk=user_id)
        posts = user.post_set.all()
        relation = Relation.objects.filter(from_user=request.user, to_user=user)
        if relation.exists():
            is_following = True
        data = {"user": user, "posts": posts, 'is_following': is_following}
        return render(request=request, template_name=self.template_name, context=data)


class UserPasswordResetView(auth_views.PasswordResetView):
    template_name = 'account/password_reset_form.html'
    success_url = reverse_lazy('account:user_password_reset_done')
    email_template_name = 'account/password_reset_email.html'


class UserPasswordResetDoneView(auth_views.PasswordResetDoneView):
    template_name = 'account/password_reset_done.html'


class UserPasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    template_name = 'account/password_reset_confirm.html'
    success_url = reverse_lazy('account:user_password_reset_complete')


class UserPasswordResetCompleteView(auth_views.PasswordResetCompleteView):
    template_name = 'account/password_reset_complete.html'


class UserFollowView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        user_id = kwargs.get('user_id')
        user = get_object_or_404(User, id=user_id)
        relation = Relation.objects.filter(from_user=request.user, to_user=user)
        if relation.exists():
            messages.error(request=request, message='you are already following this user', extra_tags='danger')
        else:
            Relation.objects.create(from_user=request.user, to_user=user)
            messages.success(request=request, message='you followed this user', extra_tags='success')
        return redirect('account:user_profile', user.id)


class UserUnFollowView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        user_id = kwargs.get('user_id')
        user = get_object_or_404(User, id=user_id)
        relation = Relation.objects.filter(from_user=request.user, to_user=user)
        if relation.exists():
            relation.delete()
            messages.success(request=request, message='you unfollowed this user', extra_tags='success')
        else:
            messages.error(request=request, message='you are not following this user', extra_tags='danger')
        return redirect('account:user_profile', user.id)


class EditUserView(LoginRequiredMixin, View):
    template_name = 'account/edit_profile.html'
    form_class = EditUserForm

    def get(self, request, *args, **kwargs):
        form = self.form_class(instance=request.user.profile, initial={"email": request.user.email})
        return render(request=request, template_name=self.template_name, context={'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, instance=request.user.profile)
        if form.is_valid():
            form.save()
            request.user.email = form.cleaned_data['email']
            request.user.save()
            messages.success(request=request, message='profile edited successfully', extra_tags='success')
        return redirect('account:user_profile', request.user.id)
