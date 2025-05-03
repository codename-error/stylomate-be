from fastapi import Depends
from config.firebaseConfig import get_firestore
from google.cloud.firestore import Client

from model.userModel import UserUpdateModel


class UserRepository:
    def __init__(self, db: Client = Depends(get_firestore)):
        self.db = db.collection("stylomate").document("data").collection("users")

    async def addPreference(self, uid: str, preference: str):
        try:
            # get user data form firestore
            user_data = self.db.document(uid)
            
            # update user preference
            docs = user_data
            
            docs.update({"preference": preference})

            # return true if update success
            return True

        # if error occurs, show error message
        except Exception as e:
            print(f"Error adding user: {e}")
            return False
        
    async def addImageModel(self, uid: str, image_model: str):
        try:
            # get user data form firestore
            user_data = await self.db.document(uid)
             
            # update user preference
            docs = user_data
            
            docs.update({"image_model": image_model})

            # return true if update success
            return True

        # if error occurs, show error message
        except Exception as e:
            print(f"Error adding user: {e}")
            return False
        
    async def getUserData(self, uid: str):
        try:
            # get user data form firestore
            user_data = self.db.document(uid).get()

            print(user_data)
            
            # check if user data exists
            if not user_data.exists:
                return None
            print(user_data.to_dict())
            # return user data
            return user_data.to_dict()

        # if error occurs, show error message
        except Exception as e:
            print(f"Error getting user data: {e}")
            return False
    
    async def get_preference(self, uid: str):
        try:
            # get user data form firestore
            user_data = self.db.document(uid).get()

            # check if user data exists
            if not user_data.exists:
                return None

            # return user data
            return user_data.to_dict().get("preference")

        # if error occurs, show error message
        except Exception as e:
            print(f"Error getting user data: {e}")
            return False
        
    async def update_coint(self, uid: str):
        try:
            # get user data form firestore
            user_data_ref = self.db.document(uid)
            
            user_data = user_data_ref.get()
            if not user_data.exists:
                print("user not exist")


            current_coint = user_data.to_dict().get("coint", 0)

            # kurangi koint sebesar 5 point
            update_coint = current_coint - 5
            if update_coint < 0:
                print("user not enough coint")
                return False
            
            user_data_ref.update({"coint": update_coint})

            return True
        
        except Exception as e:
            print("error updating coint for user")
            return False