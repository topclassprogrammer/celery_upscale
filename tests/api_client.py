import requests


class HTTPException(Exception):
    def __init__(self, status_code, details):
        self.status_code = status_code
        self.details = details


class APIClient:
    def __init__(self, base_url):
        self.base_url = base_url
        self.files = {}

    def _call(self, method, path, files=None):
        url = f"{self.base_url}{path}"
        response = requests.request(method, url, files=files)
        if response.status_code >= 400:
            raise HTTPException(response.status_code, response.text)
        try:
            return response.json()
        except ValueError:
            return response.content

    def create_task(self, image_path):
        return self._call("POST", "/upscale", {"image": open(image_path, "rb")})

    def get_task(self, task_id):
        return self._call("GET", f"/tasks/{task_id}")

    def get_processed_photo(self, photo_name):
        return self._call("GET", f"/processed/{photo_name}")
