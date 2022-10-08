from rest_framework.response import Response
from rest_framework.decorators import api_view
from api.serializers import CameraDataSerializer


@api_view(['POST'])
def post_licence_plate(request):
    serializer = CameraDataSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)
# oidv6 downloader ru --dataset dataset --type_data train --classes car "Vehicle registration plate" --limit 5000