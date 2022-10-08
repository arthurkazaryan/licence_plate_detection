from fastai.vision import *
import numpy as np
from utils.type_utils import from_preds_to_list
from PIL import Image


class VehicleTypeModel:

    def __init__(self, model_path: str):
        self.model = self.load_model(model_path=model_path)

    @staticmethod
    def load_model(model_path: str):

        model = load_learner(model_path)

        print('VehicleTypeDetection model is loaded.')

        return model

    def predict(self, image_path, veh_coordinates):

        image = Image.open(image_path)
        image_array = np.array(image)
        img = image_array[veh_coordinates[1]: veh_coordinates[3], veh_coordinates[0]: veh_coordinates[2]]
        img = Image.fromarray(img)
        img.save(image_path)
        self.model.data.add_test([image_path])

        preds, _ = self.model.get_preds(DatasetType.Test)
        pred_type = from_preds_to_list(preds, self.model)[0]

        return pred_type

    @classmethod
    def create_model(cls, config_object):
        model_path = config_object['VehicleTypeModel']['weights']

        return cls(
            model_path=model_path
        )
