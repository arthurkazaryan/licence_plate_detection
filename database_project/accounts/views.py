from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView
from django.shortcuts import render
from accounts.forms import RegistrationForm, LoginForm
from database.utils import DataMixin


class RegisterUser(DataMixin, CreateView):
    form_class = RegistrationForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('accounts-home')

    def get_context_data(self, *, object_list=None, **kwargs):

        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(current_page='accounts-register')

        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):

        user = form.save()
        login(self.request, user)

        return redirect('accounts-home')


class LoginUser(DataMixin, LoginView):
    form_class = LoginForm
    template_name = 'accounts/login.html'

    def get_context_data(self, *, object_list=None, **kwargs):

        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(current_page='accounts-login')

        return dict(list(context.items()) + list(c_def.items()))

    def get_success_url(self):

        return reverse_lazy('accounts-home')


def logout_user(request):
    logout(request)
    return redirect('accounts-login')


class ProfilePage(DataMixin, TemplateView, LoginRequiredMixin):
    template_name = 'accounts/accounts.html'

    def get(self, request, *args, **kwargs):

        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse_lazy(self.get_login_url()))

        context = self.get_user_context(
            current_page='accounts-home',
            user=request.user,
        )

        return render(request, self.template_name, context=context)
