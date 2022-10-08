from fastapi import APIRouter, UploadFile, File
from api.models import DetectionResult
from datetime import datetime
from detect import YoloV7Model
from color_detect import ColorModel
from type_detect import VehicleTypeModel
from utils.coordinates import get_vehicle_registration_plate
from ocr.main import get_plate_number
from ast import literal_eval
import configparser
import tempfile
import easyocr
import shutil
import os


detection_v1 = APIRouter()

config = configparser.ConfigParser()
config.read('config.ini')
yolo_v7_model = YoloV7Model.create_model(config_object=config)
color_model = ColorModel.create_model(config_object=config)
ocr_reader = easyocr.Reader(literal_eval(config['EasyOCR_finetuned']['lang_list']),
                            model_storage_directory=config['EasyOCR_finetuned']['model_storage_directory'],
                            user_network_directory=config['EasyOCR_finetuned']['user_network_directory'],
                            recog_network=config['EasyOCR_finetuned']['recog_network'],
                            gpu=True)
type_model = VehicleTypeModel.create_model(config_object=config)


@detection_v1.post('/push', tags=['detection'])
async def post_detecetion(image: UploadFile = File(...)):

    temp_dir = tempfile.gettempdir()
    temp_path = os.path.join(temp_dir, image.filename)
    with open(temp_path, 'wb') as uploaded_image:
        shutil.copyfileobj(image.file, uploaded_image)
    coordinates = yolo_v7_model.detect(temp_path)
    coordinates_veh_plate = get_vehicle_registration_plate(coordinates)

    response_data = []
    if coordinates_veh_plate:
        for veh_i, data in coordinates_veh_plate.items():
            plate_number = get_plate_number(ocr_reader, temp_path, data['vehicle_registration_plate'])
            vehicle_color = color_model.predict(temp_path, data['vehicle'])
            vehicle_type = type_model.predict(temp_path, data['vehicle'])
            response_data.append(DetectionResult(
                camera_id=1,
                date=datetime.now().isoformat(),
                vehicle_type=vehicle_type,
                color=vehicle_color,
                number=plate_number.upper(),
                vehicle=data['vehicle'],
                plate=data['vehicle_registration_plate']
            ).dict())

    os.remove(temp_path)

    return response_data
