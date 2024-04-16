FROM python:3.8.13-slim-buster


# created if the folder is not exists, if it does exists, then ignore this command
RUN mkdir -p /celery-tutorial-worker

# copy current directory and main.py to /app/
COPY . /celery-tutorial-worker/
WORKDIR /celery-tutorial-worker

RUN pip install -r requirements.txt

COPY ./services/start /start-celeryworker
RUN sed -i 's/\r$//g' /start-celeryworker
RUN chmod +x /start-celeryworker