import logging
from celery import shared_task

logger = logging.getLogger(__name__)

# creating task for celery
# ignore_result=False => by default we set to skip the result, some use case will need to skip the result such as send email
# retry, retry_policy => check readme
# bind=True => to allow to access the `self`
# max_retries=3 => check readme
# time_limit=60 => set timeout for the sending process
@shared_task(ignore_result=False, bind=True, max_retries=3, retry=True, retry_policy={
    'max_retries': 3,
    'interval_start': 0,
    'interval_step': 0.2,
    'interval_max': 0.2,
}, time_limit=60)
def add_together(self, a: int, b: int) -> int:
    try:
        return a + b
    except Exception as ex:
        logger.exception(ex)
        # retry if got exception from worker
        self.retry(countdown=3**self.request.retries)

# creating task for celery
# ignore_result=False => by default we set to skip the result, some use case will need to skip the result such as send email
@shared_task(ignore_result=False)
def multiple_together(a: int, b: int) -> int:
    return a * b