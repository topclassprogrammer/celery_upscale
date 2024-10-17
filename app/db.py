import pymongo
from cachetools import cached
from config import MONGO_DSN
from gridfs import GridFS


@cached({})
def get_fs():
    mongo = pymongo.MongoClient(MONGO_DSN)
    return GridFS(mongo['files'])
