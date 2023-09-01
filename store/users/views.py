from datetime import timedelta
from typing import Any, Dict
from uuid import uuid4

from django.contrib.auth.views import LoginView
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.utils.timezone import now
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, UpdateView

from common.views import CommonMixin

from .forms import UserLoginForm, UserProfileForm, UserRegistrationForm
from .models import EmailVerification, User


class UserLoginView(CommonMixin, LoginView):
    template_name = 'users/login.html'
    form_class = UserLoginForm
    title = 'Store - Авторизация'


class UserRegistrationView(CommonMixin, SuccessMessageMixin, CreateView):
    model = User
    form_class = UserRegistrationForm
    template_name = 'users/registration.html'
    success_url = reverse_lazy('users:login')
    success_message = '''Вы успешно зарегистрировались! На вашу почту направленно письмо, для подтверждения.'''
    title = 'Store - Регистрация'


class UserProfileView(CommonMixin, UpdateView):
    model = User
    form_class = UserProfileForm
    template_name = 'users/profile.html'
    title = 'Store - Личный кабинет'

    def get_success_url(self) -> str:
        return reverse_lazy('users:profile', args=(self.object.id))


class EmailVerificationView(CommonMixin, TemplateView):
    title = 'Store - Подтверждение электронной почты'
    template_name = 'users/email_verification.html'
    is_expired = False

    def get(self, request, *args: Any, **kwargs: Any):
        code = kwargs['code']
        user = User.objects.get(email=kwargs['email'])
        email_verifications = EmailVerification.objects.filter(user=user, code=code)
        if email_verifications.exists() and not email_verifications.first().is_expired():
            user.is_verified_email = True
            user.save()
            email_verifications.delete()

            return super(EmailVerificationView, self).get(request, *args, **kwargs)
        elif email_verifications.first().is_expired():
            email_verification = email_verifications.first()
            email_verification.code = uuid4()
            email_verification.expiration = now() + timedelta(hours=48)
            email_verification.save()
            email_verification.send_verification_email()
            self.is_expired = True
            return super(EmailVerificationView, self).get(request, *args, **kwargs)

        else:
            return HttpResponseRedirect(reverse('index'))

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super(EmailVerificationView, self).get_context_data(**kwargs)
        context['is_expired'] = self.is_expired

        return context
