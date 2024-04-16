FROM python:3.8.13-slim-buster


# created if the folder is not exists, if it does exists, then ignore this command
RUN mkdir -p /celery-tutorial

# copy current directory and main.py to /app/
COPY . /celery-tutorial/
WORKDIR /celery-tutorial

RUN pip install -r requirements.txt