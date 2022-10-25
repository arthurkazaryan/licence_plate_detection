from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.views.generic import TemplateView
from django.shortcuts import render
from licence_detection.forms import SendImageForm
from licence_detection.models import UserCamera, UserSnapshotItem, UserSnapshotProject
from licence_detection.utils import draw_on_image
from database.utils import DataMixin
import requests
import cv2


class LicenceDetectionPage(DataMixin, TemplateView, LoginRequiredMixin):
    template_name = 'licence_detection/main.html'

    def get(self, request, *args, **kwargs):

        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse_lazy(self.get_login_url()))

        image_form = SendImageForm
        cameras = UserCamera.objects.filter(user=request.user).order_by('-date')
        snapshots = UserSnapshotProject.objects.filter(user=request.user, camera=None).order_by('-date')

        context = self.get_user_context(
            current_page='licence_detection-home',
            user=request.user,
            cameras=cameras,
            snapshots=snapshots,
            image_form=image_form,
        )

        return render(request, self.template_name, context=context)

    def post(self, request, *args, **kwargs):

        send_image_form = SendImageForm(request.POST, request.FILES)
        if send_image_form.is_valid():
            data = send_image_form.cleaned_data
            file = {'upload_file': data['image_path']}
            file_type_flag = 'image'
        else:
            messages.error(request, f'Error occurred when processing data.')
            return HttpResponseRedirect(reverse('licence_detection-home'))

        try:
            response = requests.post("http://127.0.0.1:7861/api/v1/detection/push", files=file)
            response_data = response.json()
            if file_type_flag == 'image':
                user_snapshot_project = UserSnapshotProject(
                    user=request.user,
                    image=data['image_path']
                )
                user_snapshot_project.save()
                image = cv2.imread(user_snapshot_project.image.path)
                for cars_data in response_data['frame_0']:
                    user_snapshot_item = UserSnapshotItem(
                        project_id=user_snapshot_project.id,
                        color=cars_data['color'],
                        plate_number=cars_data['number'],
                    )
                    user_snapshot_item.save()
                image = draw_on_image(image, response_data['frame_0'])
                cv2.imwrite(user_snapshot_project.image.path, image)
            messages.success(request, f'Project has been successfully created.')
        except:
            messages.error(request, f'Server is currently unavailable.')

        return HttpResponseRedirect(reverse('licence_detection-home'))


class LicenceDetectionView(DataMixin, TemplateView, LoginRequiredMixin):
    template_name = 'licence_detection/view.html'

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
