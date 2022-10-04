from PIL import Image
import numpy as np


def get_plate_number(reader, image_path, coordinates):
    plate_number = ''
    plate_coords = coordinates.get('vehicle_registration_plate')
    if plate_coords:
        image = Image.open(image_path)
        image_array = np.array(image)
        plate_array = image_array[plate_coords[1]: plate_coords[3], plate_coords[0]: plate_coords[2]]
        plate_number = reader.readtext(plate_array)[0][1]

    return plate_number
