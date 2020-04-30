FROM python:3.7-slim-buster

WORKDIR /code
COPY . .

RUN apt-get update &&\
    apt-get install -y binutils libproj-dev gdal-bin python-gdal python3-gdal
RUN pip install -r requirements.txt
CMD ["gunicorn", "-c", "config/gunicorn/conf.py", "--bind", ":80", "--chdir", "geoproject", "geoproject.wsgi:application"]

