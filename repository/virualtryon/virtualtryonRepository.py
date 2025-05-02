from fastapi import Depends
from google.cloud.firestore import Client
from config.firebaseConfig import get_firestore


class VirtualTryOn:
    def __init__(self, db: Client = Depends(get_firestore)):
        pass