import os

from flask import Flask
from celery import Celery, Task
from celery_redis_cluster_backend.redis_cluster import RedisClusterBackend

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
    # url for local redis
    # redis_url = "redis://localhost:6379"
    # url for docker redis
    # redis_url = "redis://redis:6379/0"
    app.config.from_mapping(
        CELERY=dict(
            broker_url=os.getenv("REDIS_BROKER_URL"),
            result_backend=os.getenv("CELERY_RESULT_BACKEND"),
            task_ignore_result=True,
            # import the tasks
            imports = ('services.test_service',),
            CELERY_REDIS_CLUSTER_SETTINGS={ 'startup_nodes': [
                {"host": "redis1", "port": "6390"},
                {"host": "redis2", "port": "6391"},
                {"host": "redis3", "port": "6392"}
            ]}
        ),
    )
    app.config.from_prefixed_env()
    celery_init_app(app)
    return app


flask_app = create_app()
celery_app = flask_app.extensions["celery"]