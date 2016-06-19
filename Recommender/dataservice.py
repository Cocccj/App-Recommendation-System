from pymongo import MongoClient
import random

class DataService(object):

    @classmethod
    def init(cls, client):
        cls.client = client;
        cls.db = client.appstore;
        cls.user_download_history = cls.db.user_download_history
        cls.app_info = cls.db.app_info

    @classmethod
    def retrieve_app_info(cls, dict = {}):
        result = {}
        cursor = cls.app_info.find(dict)
        for app in cursor:
            result[app['app_id']] = {'title': app['title']}
        return result

    @classmethod
    def retrieve_user_download_history(cls, dict = {}):
        result = {}
        cursor = cls.user_download_history.find(dict)
        for user_download_history in cursor:
            result[user_download_history['user_id']] = user_download_history['download_history']
        return result

    @classmethod
    def update_app_info(cls, filterd, update_info):
        cls.app_info.update_one(filterd, update_info, True)
