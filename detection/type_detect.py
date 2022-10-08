from fastai.vision import *
from utils.type_utils import from_preds_to_list
from PIL import Image
import tempfile
import uuid


class VehicleTypeModel:

    def __init__(self, model_path: str):
        self.model = self.load_model(model_path=model_path)

    @staticmethod
    def load_model(model_path: str):

        model = load_learner(model_path)

        print('VehicleTypeDetection model is loaded.')

        return model

    def predict(self, image_array, veh_coordinates):

        img = image_array[veh_coordinates[1]: veh_coordinates[3], veh_coordinates[0]: veh_coordinates[2]]
        img = Image.fromarray(img)
        temp_dir = tempfile.gettempdir()
        image_path = os.path.join(temp_dir, f"{str(uuid.uuid4())}.jpg")
        img.save(image_path)
        self.model.data.add_test([image_path])

        preds, _ = self.model.get_preds(DatasetType.Test)
        pred_type = from_preds_to_list(preds, self.model)[0]

        os.remove(image_path)

        return pred_type

    @classmethod
    def create_model(cls, config_object):
        model_path = config_object['VehicleTypeModel']['weights']

        return cls(
            model_path=model_path
        )
