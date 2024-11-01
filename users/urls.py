from django.contrib.auth import logout
from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView, PasswordResetDoneView, \
    PasswordResetConfirmView, PasswordResetCompleteView
from django.contrib.messages import success
from django.urls import path, reverse_lazy

from users import views
from users.apps import UsersConfig
from users.views import RegisterView, ProfileView, EmailConfirmationSentView, UserConfirmEmailView, EmailConfirmedView, \
    EmailConfirmationFailedView

app_name=UsersConfig.name

urlpatterns = [
    path('',LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/',LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('profile/', ProfileView.as_view(), name='profile'),

    path('email_confirmation_sent/', EmailConfirmationSentView.as_view(), name='email_confirmation_sent'),
    path('confirm_email/<str:uid>/<str:token>/', UserConfirmEmailView.as_view(), name='confirm_email'),
    path('email_confirmed/', EmailConfirmedView.as_view(), name='email_confirmed'),
    path('confirm_email_failed/', EmailConfirmationFailedView.as_view(), name='email_confirmation_failed'),

    #Урлы для сброса пароля -------------
    path('password_reset/',
         PasswordResetView.as_view(
             template_name="users/password_reset_form.html",
             email_template_name="users/password_reset_email.html",
             success_url=reverse_lazy("users:password_reset_done")),
         name='password_reset'),

    path('password_reset/done/',
         PasswordResetDoneView.as_view(template_name="users/password_reset_done.html"),
         name='password_reset_done'),

    path('password_reset/<uidb64>/<token>/',
         PasswordResetConfirmView.as_view(
             template_name="users/password_reset_confirm.html",
             success_url=reverse_lazy("users:password_reset_complete")),
         name='password_reset_confirm'),

    path('password_reset/complete/',
         PasswordResetCompleteView.as_view(template_name="users/password_reset_complete.html"),
         name="password_reset_complete")
]