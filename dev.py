import time
from flask import Flask
from celery.result import AsyncResult
from services.test_service import add_together, multiple_together

app = Flask(__name__)

@app.route('/')
def hello_world():
    # call to celery task
    result_add_together_task = add_together_task()
    id = result_add_together_task.get('result_id')
    print(id) # get id from the celery task

    # check result
    # it should return this:
    # {'ready': False, 'successful': None, 'value': None}
    result_dict = check_result(id)
    print(result_dict)
    
    # call to another celery task
    multiple_together_task()

    time.sleep(3) # sleep for 3 seconds to see that the task is running good in background

    # check result
    # it should return this:
    # {'ready': True, 'successful': True, 'value': 5}
    result_dict = check_result(id)
    print(result_dict)

    return 'Hello, World!'


def add_together_task():
    result = add_together.delay(3, 2)  # call to celery task
    return {"result_id": result.id}


def multiple_together_task():
    result = multiple_together.delay(3, 2)  # call to celery task
    return {"result_id": result.id}


def check_result(id):
    # check the result by celery task id
    result = AsyncResult(id)
    ready = result.ready()
    result_dict = {
        "ready": ready,
        "successful": result.successful() if ready else None,
        "value": result.get() if ready else result.result,
    }
    return result_dict


if __name__ == '__main__':
    app.run()