
import os
import json
import firebase_admin
from firebase_admin import credentials, firestore
from dotenv import load_dotenv

load_dotenv()

def get_firestore():
    if not firebase_admin._apps:
        service_account = os.getenv("FIREBASE_SERVICE_ACCOUNT")

        if not service_account:
            raise ValueError("Variabel lingkungan FIREBASE_SERVICE_ACCOUNT tidak ditemukan.")
        
        try:
            service_account_dict = json.loads(service_account)
        except json.JSONDecodeError as e:
            raise ValueError(f"JSON tidak valid: {e}")

        cred = credentials.Certificate(service_account_dict)
        firebase_admin.initialize_app(cred, {
            'storageBucket': 'mobile-aplication-34f11.appspot.com'
        })
    return firestore.client()