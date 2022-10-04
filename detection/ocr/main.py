from PIL import Image
import numpy as np


def get_plate_number(reader, image_path, coordinates):

    response = '<unknown>'
    image = Image.open(image_path)
    image_array = np.array(image)
    plate_array = image_array[coordinates[1]: coordinates[3], coordinates[0]: coordinates[2]]
    plate_number = reader.readtext(plate_array)
    if plate_number:
        response = plate_number[0][1]

    return response
