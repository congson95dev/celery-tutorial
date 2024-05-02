import os

from flask import Flask
from celery import Celery, Task

sqs_queue_url = os.getenv("SQS_QUEUE_URL")
aws_access_key = os.getenv("AWS_ACCESS_KEY")
aws_secret_key = os.getenv("AWS_SECRET_KEY")
region = os.getenv("REGION")

# Generate the Celery config and assign it to Flask config

def celery_init_app(app: Flask) -> Celery:
    class FlaskTask(Task):
        def __call__(self, *args: object, **kwargs: object) -> object:
            with app.app_context():
                return self.run(*args, **kwargs)

    celery_app = Celery(app.name, task_cls=FlaskTask)
    celery_app.config_from_object(app.config["CELERY"])
    celery_app.set_default()
    app.extensions["celery"] = celery_app
    return celery_app


def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_mapping(
        CELERY=dict(
            broker_url=f"sqs://{aws_access_key}:{aws_secret_key}@",
            broker_transport_options={
                "region": region,
                "predefined_queues": {
                    "celery": {
                        "url": sqs_queue_url,
                        "access_key_id": aws_access_key,
                        "secret_access_key": aws_secret_key,
                    }
                },
            },
            task_ignore_result=True,
            # import the tasks
            imports = ('services.test_service',)
        ),
    )
    app.config.from_prefixed_env()
    celery_init_app(app)
    return app


flask_app = create_app()
celery_app = flask_app.extensions["celery"]