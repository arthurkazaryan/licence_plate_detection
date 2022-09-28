from rest_framework import serializers
from database.models import CameraData


class CameraDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = CameraData
        fields = '__all__'
