import easyocr
import cv2
import matplotlib.pyplot as plt
import numpy as np
from time import time
image_path = 'plate7.png'

reader = easyocr.Reader(['en'], gpu=True)
cur_time = time()
print('start predict')
result = reader.readtext(image_path)

print(result)
print(result[0][1])
print(time() - cur_time)
