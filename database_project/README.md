<h1 align="center">Django-based web service for licence plate detection.</h1>
<p align="center"><img src="./misc/main.jpg" alt="main" width="100%"></p>
<br>

The service is a part of a licence plate detection project and allows to send an images via the interface to Detection API and plot the results.

In order to launch make sure to be located at ``./licence_plate_detection/database_project`` directory.

First launch:
```
conda create -n django_database python=3.7
conda activate django_database
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

Second and subsequent launches:
```
conda activate django_database
python manage.py runserver
```

<b>Note:</b> only image-based detection is available by the current interface.  
