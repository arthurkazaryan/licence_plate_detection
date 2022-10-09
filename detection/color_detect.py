import cv2
import numpy as np
import tensorflow as tf


class ColorModel:

    def __init__(self, model_path: str):
        self.model = self.load_model(model_path=model_path)

    @staticmethod
    def load_model(model_path: str):

        model = tf.keras.models.load_model(model_path)

        print('ColorDetection model is loaded.')

        return model

    def predict(self, image_array, veh_coordinates):

        img = image_array[veh_coordinates[1]: veh_coordinates[3], veh_coordinates[0]: veh_coordinates[2]]
        img = np.expand_dims(cv2.resize(img, (100, 100), cv2.INTER_AREA), axis=0)

        id_color = {0: 'black', 1: 'blue', 2: 'cyan', 3: 'gray', 4: 'green', 5: 'red', 6: 'white', 7: 'yellow'}
        pred_color = id_color[np.argmax(self.model.predict(img))]

        return pred_color

    @classmethod
    def create_model(cls, config_object):
        model_path = config_object['ColorModel']['weights']

        return cls(
            model_path=model_path
        )
