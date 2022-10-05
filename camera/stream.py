import cv2
import subprocess as sp

rtsp_server = 'rtsp://rtsp_simple_server:8554/mystream'
cap = cv2.VideoCapture('car_video.mp4')
sizeStr = str(int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))) + 'x' + str(int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
fps = int(cap.get(cv2.CAP_PROP_FPS))

command = ['ffmpeg',
           '-re',
           '-s', sizeStr,
           '-r', str(fps),  # rtsp fps (from input server)
           '-i', '-',

           # You can change ffmpeg parameter after this item.
           '-pix_fmt', 'yuv420p',
           '-r', '30',  # output fps
           '-g', '50',
           '-c:v', 'libx264',
           '-b:v', '2M',
           '-bufsize', '64M',
           '-maxrate', "4M",
           '-preset', 'veryfast',
           '-rtsp_transport', 'tcp',
           '-segment_times', '5',
           '-f', 'rtsp',
           rtsp_server]

process = sp.Popen(command, stdin=sp.PIPE)
idx = 0
while cap.isOpened():
    print(f'frame {idx}')
    ret, frame = cap.read()
    if ret:
        try:
            ret2, frame2 = cv2.imencode('.png', frame)
            process.stdin.write(frame2.tobytes())
        except:
            pass
    else:
        idx = 0
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        continue
    idx += 1
