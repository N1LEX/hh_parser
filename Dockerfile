FROM python:3.8-alpine

COPY requirements.txt requirements.txt
RUN python -m pip install --upgrade pip
RUN python -m pip install -r requirements.txt
COPY . /app
WORKDIR /app