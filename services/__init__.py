import os

from flask import Flask
from celery import Celery, Task

# Generate the Celery config and assign it to Flask config

def celery_init_app(app: Flask) -> Celery:
    class FlaskTask(Task):
        def __call__(self, *args: object, **kwargs: object) -> object:
            with app.app_context():
                return self.run(*args, **kwargs)

    celery_app = Celery("tasks", task_cls=FlaskTask)
    celery_app.config_from_object(app.config["CELERY"])
    celery_app.set_default()
    app.extensions["celery"] = celery_app
    return celery_app


def create_app() -> Flask:
    app = Flask(__name__)
    # url for local redis
    # redis_url = "redis://localhost:6379"
    # url for docker redis
    # redis_url = "redis://redis:6379/0"
    # => this will help to connect within docker environment
    # redis_url = "redis://{redis_docker_ip}:6379/0"
    # => this will help to connect outside of docker environment
    # => to find redis_docker_ip, use `docker inspect celery-tutorial-redis-1` and check in `IPAddress` field
    app.config.from_mapping(
        CELERY=dict(
            broker_url=os.getenv("REDIS_BROKER_URL"),
            result_backend=os.getenv("REDIS_BROKER_URL"),
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