from django.shortcuts import render
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from django.contrib.auth.views import PasswordChangeView
from django.conf import settings
from django.core.exceptions import PermissionDenied

from users.forms import LoginUserForm, RegisterUserForm, ProfileUserForm, UserPasswordChangeForm
from library.models import BorrowRecords

class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'users/login.html'
    extra_context = {'title': 'Авторизация'}
    
class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:register_done')
    extra_context = {'title': 'Регистрация'}

class ProfileUser(LoginRequiredMixin, UpdateView):
    model = get_user_model()
    form_class = ProfileUserForm
    template_name = 'users/profile.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f"Профиль пользователя {self.request.user.username}"
        context['default_image'] = settings.DEFAULT_USER_IMAGE
        return context

    def get_success_url(self):
        return reverse_lazy('users:profile')
    
    def get_object(self, queryset = None):
        return self.request.user

class UserPasswordChange(PasswordChangeView):
    form_class = UserPasswordChangeForm
    success_url = reverse_lazy("users.password_change_done")
    template_name = "users/password_change_form.html"

    def dispatch(self, request, *args, **kwargs):
        if not request.user.has_usable_password():
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)
    

class BorrowList(ListView):
    template_name = 'users/borrow_list.html'
    context_object_name = 'loans'
    extra_context = {'title':'Ваш список взятых книг'}

    def get_queryset(self):
        return BorrowRecords.objects.filter(user=self.request.user.id)
