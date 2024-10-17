import cv2
import nanoid
import numpy as np
from config import MODEL_PATH, MONGO_DSN
from db import get_fs
from pymongo import MongoClient


class ReadModel:
    """Паттерн Singleton с однократным считыванием модели ИИ"""
    __instance = None
    scaler = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            cls.scaler = cv2.dnn_superres.DnnSuperResImpl.create()
            cls.scaler.readModel(MODEL_PATH)
        return cls.__instance


def upscale(image_data: bytes, image_filename: str):
    scaler = ReadModel(MODEL_PATH).scaler
    scaler.setModel("edsr", 2)
    image = cv2.imdecode(np.frombuffer(image_data, np.uint8), cv2.IMREAD_COLOR)
    result = scaler.upsample(image)
    extension = "." + image_filename.split('.')[-1]
    _, buffer = cv2.imencode(extension, result)
    byte_image = bytes(buffer)

    upscaled_name = "upscaled_" + nanoid.generate() + "_" + image_filename
    files = get_fs()
    with MongoClient(MONGO_DSN):
        files.put(byte_image, filename=upscaled_name)
    return upscaled_name
