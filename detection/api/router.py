from fastapi import APIRouter, UploadFile, File, status
from api.models import DetectionResult
from fastapi.responses import JSONResponse
from datetime import datetime
from detect import YoloV7Model
from ocr.main import get_plate_number
import configparser
import tempfile
import easyocr
import shutil
import os

detection_v1 = APIRouter()

config = configparser.ConfigParser()
config.read('config.ini')
yolo_v7_model = YoloV7Model.create_model(config_object=config)
ocr_reader = easyocr.Reader(['en'], gpu=True)


@detection_v1.post('/push', tags=['detection'])
async def post_detecetion(image: UploadFile = File(...)):

    temp_dir = tempfile.gettempdir()
    temp_path = os.path.join(temp_dir, image.filename)
    with open(temp_path, 'wb') as uploaded_image:
        shutil.copyfileobj(image.file, uploaded_image)
    coordinates = yolo_v7_model.detect(temp_path)
    plate_number = get_plate_number(ocr_reader, temp_path, coordinates)
    print('COORDINATES', coordinates)
    print('PLATE NUMBER', plate_number)
    os.remove(temp_path)

    return JSONResponse(
        content=DetectionResult(
            camera_id=1,
            date=datetime.now().isoformat(),
            vehicle_type='cargo',
            color='white',
            number=plate_number.upper() if isinstance(plate_number, str) else 'ERROR!!!'
        ).dict(),
        status_code=status.HTTP_202_ACCEPTED
    )
