def get_plate_number(reader, image_array, coordinates):

    response = '<unknown>'
    plate_array = image_array[coordinates[1]: coordinates[3], coordinates[0]: coordinates[2]]
    plate_number = reader.readtext(plate_array)
    if plate_number:
        response = plate_number[0][1]

    return response
