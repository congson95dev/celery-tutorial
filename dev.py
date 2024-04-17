from flask import Flask
from celery import Celery

app = Flask(__name__)

celery_app = Celery("tasks", broker="redis://172.22.0.2:6379/0", backend="redis://172.22.0.2:6379/0")

@app.route('/test')
def test():
    result = celery_app.send_task("services.test_service.add_together", args=[4, 5])    
    print(result.get())
    return 'Hello, World!'

if __name__ == '__main__':
    app.run()