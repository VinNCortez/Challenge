import firebase_admin
from firebase_admin import credentials, firestore

from settings import settings
from functools import lru_cache


@lru_cache()
def get_database():
    credential = credentials.Certificate(settings.DATABASE_CERTIFICATE)
    firebase_admin.initialize_app(credential)
    database = firestore.client()
    return database