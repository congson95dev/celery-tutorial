import time
from flask import Flask
from celery.result import AsyncResult
from services.test_service import add_together, multiple_together

app = Flask(__name__)

@app.route('/')
def hello_world():
    # call to celery task
    add_together_task()
    
    # call to another celery task
    multiple_together_task()

    return 'Hello, World!'


def add_together_task():
    result = add_together.delay(3, 2)  # call to celery task
    return {"result_id": result.id}


def multiple_together_task():
    result = multiple_together.delay(3, 2)  # call to celery task
    return {"result_id": result.id}


if __name__ == '__main__':
    app.run()