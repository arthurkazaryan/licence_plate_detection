from tqdm import tqdm
from utils import class_id
import pandas as pd
import imagesize
import os
import concurrent.futures


def download_sample(sample_id):
    car_data = car[car['ImageID'] == sample_id]
    plate_data = plate[plate['ImageID'] == sample_id]
    # dataframe_full = dataframe_full.append(car_data).append(plate_data)

    command = f'aws s3 --no-sign-request --only-show-errors cp s3://open-images-dataset/train/{sample_id}.jpg "./dataset"'
    os.system(command)
    width, height = imagesize.get(f"./dataset/{sample_id}.jpg")

    with open(f"./dataset/labels/{sample_id}.txt", 'w') as coords_txt:
        for row in car_data[['XMin', 'YMin', 'XMax', 'YMax']].values.tolist():
            row = row[0] * width, row[1] * height, row[2] * width, row[3] * height
            coords_txt.write('car ' + ' '.join(map(str, row)) + '\n')
        for row in plate_data[['XMin', 'YMin', 'XMax', 'YMax']].values.tolist():
            row = row[0] * width, row[1] * height, row[2] * width, row[3] * height
            coords_txt.write('vehicle_registration_plate ' + ' '.join(map(str, row)) + '\n')


images = pd.read_csv('./boxes/oidv6-train-annotations-bbox.csv')

car = images[images['LabelName'] == class_id['Car']]
car_ids = set(car['ImageID'].to_list())

plate = images[images['LabelName'] == class_id['Vehicle registration plate']]
plate_ids = set(plate['ImageID'].to_list())

images_id = list(car_ids.intersection(plate_ids))
print('Images to load: ', len(images_id))

dataframe_full = pd.DataFrame.from_dict({key: [] for key in images.columns})

with concurrent.futures.ThreadPoolExecutor() as executor:
    results = executor.map(download_sample, images_id)
    for _ in tqdm(results):
        pass
