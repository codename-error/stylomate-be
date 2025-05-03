import base64
from fastapi import Depends, HTTPException, UploadFile
from requests import request

from model.userModel import AddRequestImageModel, UserUpdateModel
from repository.user.userRepository import UserRepository
from utils.tokenJWT import TokenData
from PIL import Image
from rembg import remove
from io import BytesIO


class UserService:
    def __init__(self, userRepository: UserRepository = Depends()):
        self.userRepository = userRepository

    async def addPreference(self, current_user: TokenData, request: UserUpdateModel):
        try:
            # get uid
            uid = current_user.uid

            # add user preference
            await self.userRepository.addPreference(uid, request.preference)
            return {
                "message": "success add preference",
                "preference": request.preference
            }

        # jika terjadi error, tampilkan pesan error
        except Exception as e:
            return HTTPException(
                status_code=500,
                detail=f"Error adding preference: {e}"
            )
        
    async def addImageModel(self, current_user: TokenData, file_base64: AddRequestImageModel):
        try:
            # get uid
            uid = current_user.uid

            file = request.file

            image_data = base64.b64decode(file)
            # Open image using PIL
            input_image = Image.open(BytesIO(image_data)).convert("RGBA")
           
  
            output = remove(input_image)

            if output.mode != "RGBA":
                print("image not RGBA")
                output.convert("RGBA")
            
            # menggunakan penyimpanan sementara
            buffered = BytesIO()
            output.save(buffered, format="PNG")
            # reset ke pointer 0
            buffered.seek(0)

            image_data = buffered.getvalue()

            img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")

            # add user preference
            result = await self.userRepository.addImageModel(uid, img_str)
            return {
                "message": "success add image model",

            }

        # jika terjadi error, tampilkan pesan error
        except Exception as e:
            return HTTPException(
                status_code=500,
                detail=f"Error adding image model: {e}"
            )
        
    async def getUserData(self, current_user: TokenData):
        try:
            # get uid
            uid = current_user.uid

            # get user data
            user_data = await self.userRepository.getUserData(uid)

            # return user data
            return {
                "message": "success get user data",
                "data": user_data['image_model']
            }

        # jika terjadi error, tampilkan pesan error
        except Exception as e:
            return HTTPException(
                status_code=500,
                detail=f"Error getting user data: {e}"
            )

        