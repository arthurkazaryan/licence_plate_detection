from utils.datasets import LoadImages
from utils.torch_utils import select_device
from utils.general import check_img_size
from PIL import Image
from ast import literal_eval
import numpy as np
import tensorflow as tf


class ColorModel:

    def __init__(self, model_path: str, device_type: str, img_size: int,):
        self.model, self.device = self.load_model(
            model_path=model_path,
            device_type=device_type,
            img_size=img_size
        )
        self.names = self.model.module.names if hasattr(self.model, 'module') else self.model.names
        self.img_size = img_size

    @staticmethod
    def load_model(model_path: str, device_type: str, no_trace: bool, img_size: int):
        device = select_device(device_type)
        half = device.type != 'cpu'

        model = tf.keras.models.load_model(model_path)

        if half:
            model.half()  # to FP16
        print('Model loaded.')

        return model, device

    def predict(self, image_path, veh_coordinates):

        image = Image.open(image_path)
        image_array = np.array(image)
        img = image_array[veh_coordinates[1]: veh_coordinates[3], veh_coordinates[0]: veh_coordinates[2]]

        id_color = {0:'black', 1:'blue', 2:'cyan', 3:'gray', 4:'green', 5:'red', 6:'white', 7:'yellow'}
        pred_color = id_color[np.argmax(model.predict(img))]

        return pred_color, img

    @classmethod
    def create_model(cls, config_object):
        model_path = config_object['ColorModel']['weights']
        device_type = config_object['ColorModel']['device_type']
        img_size = literal_eval(config_object['ColorModel']['img_size'])

        return cls(
            model_path=model_path,
            device_type=device_type,
            img_size=img_size,
        )
