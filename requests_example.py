import time

import requests

BASE_URL = "http://127.0.0.1:5000"


def create_task(image_path) -> str:
    resp = requests.post(f"{BASE_URL}/upscale",
                         files={"image": open(f"{image_path}", "rb")})
    print(resp.json())
    return resp.json()['task_id']


def get_task(task_id) -> str:
    status = None
    while status != 'SUCCESS':
        resp = requests.get(f"{BASE_URL}/tasks/{task_id}")
        status = resp.json()['status']
        time.sleep(2)
        print(resp.json())
    return resp.json()['result'].split('/processed/')[1]


def get_processed_image(image_name) -> bytes:
    resp = requests.get(f"{BASE_URL}/processed/{image_name}")
    print(resp.content)
    return resp.content


if __name__ == '__main__':
    task_id = create_task("images/lama_300px.png")
    image_name = get_task(task_id)
    processed_image = get_processed_image(image_name)
