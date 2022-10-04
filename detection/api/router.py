from fastapi import APIRouter, UploadFile, File, status
from api.models import DetectionResult
from fastapi.responses import JSONResponse
from datetime import datetime
from detect import YoloV7Model
from color_detect import ColorModel
# from type_detect import VehicleTypeModel
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
    plate_number = get_plate_number(ocr_reader, temp_path, coordinates)
    print('COORDINATES', coordinates)
    print('PLATE NUMBER', plate_number)
    os.remove(temp_path)
        
    veh_coordinates = [coor_i for coor_i in coordinates['car']
                               if coor_i[0] < coordinates['vehicle_registration_plate'][0][0] and
                                  coor_i[1] < coordinates['vehicle_registration_plate'][0][1] and
                                  coor_i[2] > coordinates['vehicle_registration_plate'][0][2] and
                                  coor_i[3] > coordinates['vehicle_registration_plate'][0][3]]

    print('VEHICLE COORDINATES', veh_coordinates)
    if veh_coordinates != []:

        vehicle_color, veh_img = color_model.predict(temp_path, veh_coordinates[0])
        print('COLOR', vehicle_color)
        print(veh_img)

        # vehicle_type = '' # v_type_model.predict(veh_img)
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
