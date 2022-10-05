FROM python:3.7-slim

ENV PYTHONUNBUFFERED 1
COPY ./requirements.txt /requirements.txt

RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6  -y
RUN pip install -r /requirements.txt

RUN mkdir /camera
COPY ./ /camera
WORKDIR ./camera
