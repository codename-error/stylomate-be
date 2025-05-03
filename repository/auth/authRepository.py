
from fastapi import Depends
from google.cloud.firestore import Client
from config.firebaseConfig import get_firestore
from model.userModel import UserModel


class AuthRepository:
    def __init__(self, db: Client = Depends(get_firestore)):
        self.db = db.collection("stylomate").document("data")

    # menambahkan user baru ke dalam collection users
    async def addUserRegister(self, uid: str,user_data: UserModel):
        try:
            print(user_data.id)
            # menambahkan user baru ke dalam collection users
            await self.db.collection("users").document(uid).set({
                "id": user_data.id,
                "email": user_data.email,
                "username": user_data.username,
                "password": user_data.password,
                "profile_picture": user_data.profile_picture or "",
                "preference": user_data.preference or [],
                "image_model": user_data.image_model or "",
            })
            return True
        
        # jika terjadi error, tampilkan pesan error
        except Exception as e:
            print(f"Error adding user: {e}")
            return False

    async def getUserData(self, uid: str):

        data = self.db.collection("users").document(uid).get()
        if data.exists:

            user = UserModel(**data.to_dict())
            return user.model_dump()
        else:
            return None

    




