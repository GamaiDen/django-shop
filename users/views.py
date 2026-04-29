from django.shortcuts import redirect
from django.contrib.auth import login, logout, authenticate
from django.urls import reverse_lazy
from django.views.generic import CreateView, FormView
from django.core.mail import send_mail
from django.conf import settings
from .forms import RegisterForm, LoginForm
from .models import User


class RegisterView(CreateView):
    model = User
    form_class = RegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        response = super().form_valid(form)
        user = self.object
        send_mail('Добро пожаловать!', f'Привет, {user.email}!', settings.DEFAULT_FROM_EMAIL, [user.email], fail_silently=True)
        return response


class LoginView(FormView):
    form_class = LoginForm
    template_name = 'users/login.html'

    def form_valid(self, form):
        email = form.cleaned_data['email']
        password = form.cleaned_data['password']
        user = authenticate(self.request, username=email, password=password)
        if user:
            login(self.request, user)
            return redirect('home')
        form.add_error(None, 'Неверный email или пароль.')
        return self.form_invalid(form)


def logout_view(request):
    logout(request)
    return redirect('home')
