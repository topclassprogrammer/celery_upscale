import io

import celery
from celery_app import celery_app, get_task, upscale_photos
from config import MONGO_DSN
from db import get_fs
from flask import Flask, jsonify, request, send_file
from flask.views import MethodView
from flask_pymongo import PyMongo
from gridfs.errors import NoFile
from pymongo import MongoClient

app = Flask("app")
mongo = PyMongo(app=app, uri=MONGO_DSN)
celery_app.conf.update(app.config)


class ContextTask(celery.Task):
    def __call__(self, *args, **kwargs):
        with app.app_context():
            return self.run()


celery.Task = ContextTask


class UpScaleView(MethodView):
    def get(self, task_id):
        task = get_task(task_id)
        if task.result:
            self.get_file(task.result)
            return jsonify({
                "status": task.status,
                "result": f"http://127.0.0.1:5000/processed/{task.result}"})
        else:
            return jsonify({"status": task.status})

    @staticmethod
    @app.route("/processed/<filename>")
    def get_file(filename):
        files = get_fs()
        try:
            with MongoClient(MONGO_DSN):
                target_file = files.get_last_version(filename)
        except NoFile:
            return jsonify({"status": "not found"})
        else:
            return send_file(
                io.BytesIO(target_file.read()),
                mimetype=target_file.content_type, download_name=filename)

    def post(self):
        image = request.files.get('image')
        image_data = image.stream.read()
        image_filename = image.filename
        task = upscale_photos.delay(image_data, image_filename)
        return jsonify({"task_id": task.id})


upscale_view = UpScaleView.as_view('upscale')
app.add_url_rule(rule='/upscale', view_func=upscale_view, methods=['POST'])
app.add_url_rule(rule='/tasks/<task_id>', view_func=upscale_view, methods=['GET'])
