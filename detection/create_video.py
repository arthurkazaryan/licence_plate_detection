from argparse import ArgumentParser
from pathlib import Path
import requests
import cv2

post_url = 'http://127.0.0.1:7861/api/v1/detection/push'


def detect(file_path: Path):
    save_file_path = Path(file_path.parent, 'processed_' + file_path.name)

    video_read = cv2.VideoCapture(str(file_path))
    height = video_read.get(cv2.CAP_PROP_FRAME_HEIGHT)
    width = video_read.get(cv2.CAP_PROP_FRAME_WIDTH)
    fps = video_read.get(cv2.CAP_PROP_FPS)

    fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
    video_write = cv2.VideoWriter(str(save_file_path), fourcc, fps, (int(width), int(height)))

    file = open(file_path, 'rb')
    try:
        resp = requests.post(url=post_url, files={'upload_file': file})
        api_response = resp.json()
    except:
        print('Server is unavailable')
        file.close()
        raise

    frame_idx = 0
    frame_data = list(api_response.values())
    while frame_idx < len(frame_data):
        ret, image = video_read.read()
        for data in frame_data[frame_idx]:
            veh_co = data['vehicle']
            pl_co = data['plate']
            image = cv2.rectangle(image, veh_co[:2], veh_co[2:], (0, 0, 255), 2)
            image = cv2.rectangle(image, pl_co[:2], pl_co[2:], (0, 255, 255), 2)

            image = cv2.putText(image, data['number'], pl_co[:2], cv2.FONT_HERSHEY_COMPLEX, 1.5, (0, 255, 255), 3, 2)
            image = cv2.putText(image, f"Color: {data['color']}", veh_co[:2], cv2.FONT_HERSHEY_COMPLEX, 1.5,
                                (0, 0, 255), 3, 2)
        video_write.write(image)
        frame_idx += 1

    video_read.release()
    video_write.release()

    return save_file_path


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument("--file_path", type=str, help="path to a file")
    args = parser.parse_args()

    saved_file = detect(Path(args.file_path))
    print(f'File is saved at: {Path.cwd().joinpath(saved_file)}')
