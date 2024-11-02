from email.message import EmailMessage
from multiprocessing.dummy import current_process
from random import randint

from django.contrib.auth import login, get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import PasswordResetView
from django.contrib.sites.models import Site
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse_lazy, reverse
from django.utils.crypto import get_random_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views import View
from django.views.generic import CreateView, UpdateView, TemplateView
from django.utils.encoding import force_bytes

from config import settings
from users.forms import UserRegisterForm, UserProfileForm
from users.models import User
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode



class ProfileView(LoginRequiredMixin,UpdateView):
    model = User
    form_class = UserProfileForm
    success_url = reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user

class UserConfirmEmailView(View):
    def get(self, request, uid, token):
        user = get_object_or_404(User, pk=uid, verification_token=token)
        user.is_active = True
        user.save()
        return render(request, 'users/email_confirmed.html')


class RegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:email_confirmation_sent')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Регистрация на сайте'
        return context

    def form_valid(self, form):
        response =super().form_valid(form)
        user = form.save(commit=False)

        # Функционал для отправки письма и генерации токена
        token = get_random_string(length=50)
        user.verification_token = token
        user.save()
        #Отправляем письмо с подтверждением
        current_site =get_current_site(self.request)
        subject = 'Подтвердите свой электронный адрес'
        message = (f'Пожалуйста, перейдите по следующей ссылке, чтобы подтвердить свой адрес'
                   f' электронной почты: http://{current_site.domain}{reverse("users:confirm_email",kwargs={"uid": user.pk, "token": token})}')

        send_mail(
            subject=subject,
            message=message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[self.object.email],
            fail_silently=False,
        )
        return redirect(self.success_url)



class EmailConfirmationSentView(TemplateView):
    template_name = 'users/email_confirmation_sent.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Письмо активации отправлено'
        return context

class EmailConfirmedView(TemplateView):
    template_name = 'email_confirmed.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Ваш электронный адрес Октивирован'
        return context

class EmailConfirmationFailedView(TemplateView):
    template_name = 'email_confirmation_failed.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Ваш электронный адрес не активирован"
        return context

