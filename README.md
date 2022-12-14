<h1 align="center">Licence plate detection</h1>
<p align="center"><img src="./database_project/misc/main.jpg" alt="scheme" width="100%"></p>
<br>
The project is made as part of a deep learning course at ITMO University. The goal is to train and deploy a NN model for licence 
plate recognition. 

<p align="center"><img src="./misc/scheme.jpg" alt="scheme" width="70%"></p>
<p align="center">Overall scheme of a project</p>

<h2 align="center">Training</h2>
<hr>
<h3>Dataset collection</h3>
The dataset was downloaded from <a href="https://storage.googleapis.com/openimages/web/download.html">Open Images Dataset v6</a> using self written script, based on <a href="https://github.com/DmitryRyumin/OIDv6">OIDv6</a> package.
The main difference is that OIDv6 doesn't allow to download images, containing both "Car" and "Vehicle licence plate" classes on a single picture. 

WARNING! In order to launch the script, the annotations file ``./boxes/oidv6-train-annotations-bbox.csv`` has to be in place.

```
cd dataset
conda create -n download_oidv6
pip install -r requirements.txt
python3 download_dataset.py
```
After the script has finished, the dataset with 4000 images was loaded into the <a href="https://roboflow.com/">Roboflow</a>.

<h3>Training Yolov7</h3>
The training process of Yolov7 was done in Google Colab notebook <a href="https://github.com/arthurkazaryan/licence_plate_detection/blob/main/detection/YOLOv7_train.ipynb">(link)</a>. 
It took almost 3 hours to complete 55 epochs.
<p align="center"><img src="./misc/detection_animation.gif" alt="detection_animation" width="70%"></p>

<h2 align="center">Modules</h2>
<hr>
There are three main modules which can be launched independently in an infinite amount in order to reach maximum scalability:
<ul>
<li>Camera;</li>
<li>Detection;</li>
<li>Server.</li>
</ul>

<h3>Camera</h3>
The camera stream is using a RTSP server, which is launched on a separate Docker container.
For testing purpose, the camera is loop-streaming a short, 10 seconds video, 

``./camera/car_video.mp4``. In order to launch:

```
cd camera
docker-compose up --build
```

<h3>Detection</h3>
<img src="./detection/misc/main.jpg" alt="main" width="100%">

<br>
The detection module is wrapped around Fast API service. The main task of the module is to receive a POST request, 
containing an image or video data 

``{'upload_file': <image/video>}``
, process it, and return a json-type data, which contains the following:
<ul>
<li>date: datetime;</li>
<li>vehicle_type: str;</li>
<li>color: str;</li>
<li>number: str;</li>
<li>vehicle: list;</li>
<li>plate: list.</li>
</ul>

<p align="center"><img src="./misc/detection_scheme.jpg" alt="detection_scheme" width="70%"></p>
<p align="center">The scheme of a detection module</p>

In order to launch:

```
cd detection
conda create -n detection python=3.7
pip install -r requirements.txt
python launch_api.py
```

<h3>Django server</h3>

In order to launch:

```
cd database_project
conda create -n django_database python=3.7
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

<p align="center"><img src="./database_project/misc/view.jpg" alt="scheme" width="100%"></p>
<p align="center">View page of a detected picture</p>
