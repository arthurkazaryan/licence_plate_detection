from fastapi import APIRouter, UploadFile, File, status
from api.models import DetectionResult
from fastapi.responses import JSONResponse
from datetime import datetime
from detect import YoloV7Model
from color_detect import ColorModel
# from type_detect import VehicleTypeModel
from utils.coordinates import get_vehicle_registration_plate
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
color_model = ColorModel.create_model(config_object=config)
# v_type_model = VehicleTypeModel.create_model(config_object=config)


@detection_v1.post('/push', tags=['detection'])
async def post_detecetion(image: UploadFile = File(...)):

    temp_dir = tempfile.gettempdir()
    temp_path = os.path.join(temp_dir, image.filename)
    with open(temp_path, 'wb') as uploaded_image:
        shutil.copyfileobj(image.file, uploaded_image)
    coordinates = yolo_v7_model.detect(temp_path)
    coordinates_veh_plate = get_vehicle_registration_plate(coordinates)
    print('COORDINATES DICT', coordinates_veh_plate)

    for veh_i in range(len(coordinates_veh_plate)):
        plate_number = get_plate_number(ocr_reader, temp_path, coordinates_veh_plate['vehicle_'+str(veh_i)])
        coordinates_veh_plate['vehicle_'+str(veh_i)]['number'] = plate_number
    print('NUMBERS', coordinates_veh_plate)
    
    os.remove(temp_path)    

    if coordinates_veh_plate:
        for veh_i in range(len(coordinates_veh_plate)):
            vehicle_color, veh_img = color_model.predict(temp_path, coordinates_veh_plate['vehicle_'+str(veh_i)]['vehicle'])
            print('COLOR', vehicle_color)
            vehicle_type = '' # v_type_model.predict(veh_img)
    else:
        print('Not correct')
        vehicle_color = 'Error'
        vehicle_type = 'Error'

    return JSONResponse(
        content=DetectionResult(
            camera_id=1,
            date=datetime.now().isoformat(),
            vehicle_type=vehicle_type,
            color=vehicle_color,
            number=plate_number.upper() if isinstance(plate_number, str) else 'ERROR!!!'
        ).dict(),
        status_code=status.HTTP_202_ACCEPTED
    )
