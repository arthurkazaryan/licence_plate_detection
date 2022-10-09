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

from utils.datasets import LoadImages
from utils.general import check_img_size

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
async def post_detection(upload_file: UploadFile = File(...)):

    temp_dir = tempfile.gettempdir()
    temp_path = os.path.join(temp_dir, upload_file.filename)
    with open(temp_path, 'wb') as uploaded_file:
        shutil.copyfileobj(upload_file.file, uploaded_file)

    stride = int(yolo_v7_model.model.stride.max())
    imgsz = check_img_size(yolo_v7_model.img_size, s=stride)
    dataset = LoadImages(temp_path, img_size=imgsz, stride=stride)

    response_data = {}
    for idx, (path, img, im0s, vid_cap) in enumerate(dataset):
        response_data[f'frame_{idx}'] = []
        coordinates = yolo_v7_model.detect(img, im0s, imgsz)
        if coordinates:
            coordinates_veh_plate = get_vehicle_registration_plate(coordinates)
            for veh_i, data in coordinates_veh_plate.items():
                plate_number = get_plate_number(ocr_reader, im0s, data['vehicle_registration_plate'])
                vehicle_color = color_model.predict(im0s, data['vehicle'])
                vehicle_type = type_model.predict(im0s, data['vehicle'])
                response_data[f'frame_{idx}'].append(DetectionResult(
                    date=datetime.now().isoformat(),
                    vehicle_type=vehicle_type,
                    color=vehicle_color,
                    number=plate_number.upper(),
                    vehicle=data['vehicle'],
                    plate=data['vehicle_registration_plate']
                ).dict())

    os.remove(temp_path)

    return response_data
