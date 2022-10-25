from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.views.generic import TemplateView
from django.shortcuts import render
from text_comparison.forms import SendTextForm
from text_comparison.models import UserComparisons
from database.utils import DataMixin
import requests
import cv2


class TextComparisonPage(DataMixin, TemplateView, LoginRequiredMixin):
    template_name = 'text_comparison/main.html'

    def get(self, request, *args, **kwargs):

        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse_lazy(self.get_login_url()))

        text_form = SendTextForm
        user_comparisons = UserComparisons.objects.filter(user=request.user).order_by('-date')

        context = self.get_user_context(
            current_page='text_comparison-home',
            user=request.user,
            user_comparisons=user_comparisons,
            text_form=text_form,
        )

        return render(request, self.template_name, context=context)

    def post(self, request, *args, **kwargs):

        send_text_form = SendTextForm(request.POST)
        if send_text_form.is_valid():
            data = send_text_form.cleaned_data
        else:
            messages.error(request, f'Error occurred when processing data.')
            return HttpResponseRedirect(reverse('text_comparison-home'))

        try:
            response = requests.post("http://127.0.0.1:7761/api/v1/detection/push", params={'name': data['name']})
            response_data = response.json()
            user_comparison_project = UserComparisons(
                user=request.user,
                text=data['name'],
                nearest_text=response_data['nearest'],
                similarity=response_data['distance']
            )
            user_comparison_project.save()
            if response_data['status'] == 'FOUND':
                messages.info(request, f'Found an existing company {response_data["nearest"]} '
                                       f'with the distance {response_data["distance"]}')
            elif response_data['status'] == 'ADDED':
                messages.success(request, f'{data["name"]} has been added to database. '
                                          f'The nearest company name is {response_data["nearest"]} '
                                          f'with the distance {response_data["distance"]}')
        except:
            messages.error(request, f'Server is currently unavailable.')

        return HttpResponseRedirect(reverse('text_comparison-home'))
