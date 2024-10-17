from celery import Celery
from celery.result import AsyncResult
from config import REDIS_BACKEND_DSN, REDIS_BROKER_DSN
from upscale import upscale

celery_app = Celery("app", broker=REDIS_BROKER_DSN, backend=REDIS_BACKEND_DSN)


def get_task(task_id: str) -> AsyncResult:
    return AsyncResult(task_id, app=celery_app)


@celery_app.task
def upscale_photos(image_data, image_filename):
    return upscale(image_data, image_filename)
