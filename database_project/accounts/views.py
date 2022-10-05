from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, TemplateView, UpdateView
from django.shortcuts import render
from accounts.forms import RegistrationForm, LoginForm, SendImageForm
from accounts.models import UserCamera, UserSnapshotItem, UserSnapshotProject
# from accounts.forms import SendAPIForm
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

        image_form = SendImageForm
        cameras = UserCamera.objects.filter(user=request.user).order_by('-date')
        snapshots = UserSnapshotProject.objects.filter(user=request.user, camera=None).order_by('-date')

        context = self.get_user_context(
            current_page='accounts-home',
            user=request.user,
            cameras=cameras,
            snapshots=snapshots,
            image_form=image_form
        )

        return render(request, self.template_name, context=context)

    def post(self, request, *args, **kwargs):

        send_image_form = SendImageForm(request.POST, request.FILES)
        if send_image_form.is_valid():
            messages.success(request, f'Image has been successfully created.')
        else:
            messages.error(request, f'Error occurred when processing data.')

        return HttpResponseRedirect(reverse('accounts-home'))


class ViewPage(DataMixin, TemplateView, LoginRequiredMixin):
    template_name = 'accounts/view.html'

    def get(self, request, *args, **kwargs):

        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse_lazy(self.get_login_url()))

        context = self.get_user_context(
            user=request.user,
        )

        project_uuid = kwargs['uuid']
        project = UserSnapshotProject.objects.filter(project_uuid=project_uuid)
        data = UserSnapshotItem.objects.filter(project__id__in=project.all())

        context['project'] = project[0]
        if data:
            context['data'] = data

        return render(request, self.template_name, context=context)
