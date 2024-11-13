# users/views.py

from django.contrib.auth import login as auth_login
from django.contrib.auth import views as auth_views
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.views import LogoutView
from django.contrib.auth.forms import AuthenticationForm
from django.views.generic.edit import FormView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from .forms import CustomUserCreationForm
from django.http import HttpResponseRedirect
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from .models import UserAction


# Create your views here.
def dashboard(request):
    return render(request, 'users/dashboard.html')

def register(request):
    if request.method == 'GET':
        return render(
            request, "users/register.html",
            {"form": CustomUserCreationForm}
        )
    elif request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect(reverse("dashboard"))


class LoginView(FormView):
    form_class = AuthenticationForm
    template_name = 'users/login.html'
    success_url = reverse_lazy('invoice_list')

    def form_valid(self, form):
        auth_login(self.request, form.get_user())
        print("Vartotojas prisijungė sėkmingai")

        # return redirect(reverse_lazy('invoice_list'))
        return super().form_valid(form)  # redirects to 'success_url'

class PasswordResetDoneView(auth_views.PasswordResetDoneView):
    template_name = 'users/password_reset_done.html'
    success_url = reverse_lazy('dashboard')

class PasswordResetView(auth_views.PasswordResetView):
    template_name = 'users/password_reset_form.html'
    email_template_name = 'users/password_reset_email.html'
    success_url = reverse_lazy('password_reset_done')


class PasswordChangeDoneView(auth_views.PasswordChangeDoneView):
    template_name = 'users/password_change_done.html'
    success_url = reverse_lazy('dashboard')

@method_decorator(csrf_protect, name='dispatch')
class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('login')

    def post(self, request, *args, **kwargs):
        self.logout(request)
        return HttpResponseRedirect(self.get_next_page())

    def logout(self, request):
        auth_logout(request)

    def get_next_page(self):
        if self.request.user.is_staff:
            return reverse_lazy('users_login')
        return self.next_page

