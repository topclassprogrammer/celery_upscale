import datetime
import re
import time

from api_client import APIClient
from config import TIMEOUT_TASK


def test_task(api_client: APIClient, subtests):
    task = api_client.create_task("test.png")
    task_id = task['task_id']
    pattern = r"[0-9, a-f]{8}-[0-9, a-f]{4}-[0-9, " \
              r"a-f]{4}-[0-9, a-f]{4}-[0-9, a-f]{12}"
    # Проверка создания задачи
    assert task_id == re.match(pattern, task_id)[0]
    with subtests.test(msg='get_task'):
        task = api_client.get_task(task_id)
        assert task['status'] == 'PENDING'

    with subtests.test(msg='get_finished_task'):
        start_time = datetime.datetime.now()
        while task['status'] == 'PENDING':
            task = api_client.get_task(task_id)
            time.sleep(1)
            if task['status'] == 'SUCCESS':
                task_result = task.get('result')
                # Проверка наличия результата в задаче
                assert task_result
                break
            if start_time < datetime.datetime.now() - \
                    datetime.timedelta(seconds=TIMEOUT_TASK):
                # Проверка наличия результата в задаче после истечения таймаута
                assert task['status'] == 'SUCCESS', \
                    f'Фото не обработалось за {TIMEOUT_TASK} секунд'
                break

    with subtests.test(msg='get_processed_photo'):
        photoname = task_result.split('processed/')[1]
        response = api_client.get_processed_photo(photoname)
        # Проверка, что результат в задаче является байтовой строкой
        assert isinstance(response, bytes)
