from django.urls import path
from django.contrib.auth import views as auth_views
from .views import LoginView, dashboard, register, CustomLogoutView
from django.urls import reverse_lazy


urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('dashboard/', dashboard, name='dashboard'),
    path('password_change/', auth_views.PasswordChangeView.as_view(template_name='users/password_change_form.html'), name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='users/password_change_done.html'), name='password_change_done'),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='users/password_reset_form.html', email_template_name='users/password_reset_email.html', success_url=reverse_lazy('password_reset_done')), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'), name='password_reset_complete'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('users/login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='users_login'),
    path('register/', register, name='register'),
]

