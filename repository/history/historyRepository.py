from fastapi import Depends
from google.cloud.firestore import Client
from config.firebaseConfig import get_firestore
from datetime import datetime
from utils.generateDate import format_tanggal


class HistoryRepository:
    def __init__(self, db: Client = Depends(get_firestore)):
        self.db = db.collection("stylomate").document("data").collection("history")

    async def save_history(self, feature: str, coint: int, uid: str):
        try:
            date = format_tanggal(datetime.now())
            print("masuk sini")

            # Simpan data history langsung di collection "history", termasuk UID sebagai field
            self.db.document(uid).collection("data").add({
                "uid": uid,
                "tanggal": date,
                "feature": feature,
                "coint_use": coint
            })

            return True

        except Exception as e:
            print(f"Error saat menyimpan history: {e}")
            return False

    async def get_history(self, uid: str):
        try:
            # Query berdasarkan field uid
            query = self.db.where("uid", "==", uid).stream()
            history_list = [doc.to_dict() for doc in query]
            return history_list

        except Exception as e:
            print(f"Error saat mengambil history: {e}")
            return []