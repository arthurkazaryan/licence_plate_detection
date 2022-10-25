import cv2


def draw_on_image(image, cars_data):
    for data in cars_data:
        veh_co = data['vehicle']
        pl_co = data['plate']
        image = cv2.rectangle(image, veh_co[:2], veh_co[2:], (0, 0, 255), 2)
        image = cv2.rectangle(image, pl_co[:2], pl_co[2:], (0, 255, 255), 2)

        image = cv2.putText(image, data['number'], pl_co[:2], cv2.FONT_HERSHEY_COMPLEX, 1.5, (0, 255, 255), 3, 2)
        image = cv2.putText(image, f"Color: {data['color']}", veh_co[:2], cv2.FONT_HERSHEY_COMPLEX, 1.5, (0, 0, 255), 3, 2)

    return image
