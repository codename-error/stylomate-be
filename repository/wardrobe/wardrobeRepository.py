from fastapi import Depends
from google.cloud.firestore import Client
from config.firebaseConfig import get_firestore
from model.clothesModel import ClothesModel, UpdateClothesModel


class WardrobeRepository:
    def __init__(self, db: Client = Depends(get_firestore)):
        self.db = db.collection("stylomate").document("data").collection("wardrobe")
    
    # menambahkan clothes baru ke dalam collection clothes
    async def add_clothes(self, uid: str, id: int, type: str,color: str, length: str, category: str, pattern: str, img_str: str):
        try:
            # menambahkan user baru ke dalam collection users
            self.db.document(uid).collection("data").add({
                "id": id,
                "type": type,
                "color": color,
                "length": length,
                "category": category,
                "pattern": pattern,
                "image_url": img_str
            })
            return True

        # jika terjadi error, tampilkan pesan error
        except Exception as e:
            print(f"Error adding user: {e}")
            return False
        
    # melakukan delete clothes berdasarkan id
    async def get_clothes_by_id(self, uid: str, id: int):
        try:
            # menambahkan user baru ke dalam collection users
            get_query = self.db.document(uid).collection("data").where("id", "==", id)

            docs = get_query.stream()
            clothes_list = []
            for cloth in docs:
                clothes_list.append(cloth.to_dict())
            return clothes_list

        # jika terjadi error, tampilkan pesan error
        except Exception as e:
            print(f"Error adding user: {e}")
            return False
    
    # melakukan delete clothes berdasarkan id
    async def delete_clothes(self, uid: str, id: int):
        try:
            # menambahkan user baru ke dalam collection users
            delete_query = self.db.document(uid).collection("data").where("id", "==", id)

            docs = delete_query.stream()
            found = False
            for doc in docs:
                found = True
                doc.reference.delete()
                print(f"Document {uid} deleted successfully.")
                return True

            if not found:
                print(f"Document {uid} not found.")
                return False
        # jika terjadi error, tampilkan pesan error
        except Exception as e:
            print(f"Error adding user: {e}")
            return False
    
    async def get_clothes(self, uid: str):
        try:
            # menambahkan user baru ke dalam collection users
            clothes = self.db.document(uid).collection("data").stream()
            clothes_list = []
            for cloth in clothes:
                clothes_list.append(cloth.to_dict())
            return clothes_list

        # jika terjadi error, tampilkan pesan error
        except Exception as e:
            print(f"Error adding user: {e}")
            return False
    
    async def get_clothes_by_type(self, uid: str, type: str):
        try:
            # mengambil data berdasarkan id
            clothes = self.db.document(uid).collection("data").where("jenis", "==", type).stream()
            
            # mengambil data berdasarkan type
            clothes_list = []
            for cloth in clothes:
                clothes_list.append(cloth.to_dict())
            return clothes_list

        # jika terjadi error, tampilkan pesan error
        except Exception as e:
            print(f"Error adding user: {e}")
            return False
        
    # melakukan update clothes berdasarkan id
    async def update_clothes(self ,id: int, request: UpdateClothesModel, uid: str):
        try:
            # menambahkan user baru ke dalam collection users
            user_data = self.db.document(uid).collection("data").where("id", "==", id)
            
            docs = user_data.stream()
            for doc in docs:
                # merubah ke model pydantic
                if isinstance(request, dict):
                    request = UpdateClothesModel(**request)

                update_dict = {k: v for k, v in request.model_dump().items() if v is not None}

                doc.reference.update(update_dict)

                # mengembalikan seluruh data upadte ke klien
                return update_dict

        # jika terjadi error, tampilkan pesan error
        except Exception as e:
            print(f"Error adding user: {e}")
            return False