from fastapi import Depends
from fastapi.responses import JSONResponse
from model.userModel import AddRequestImageModel, UserUpdateModel
from service.user.userService import UserService
from utils.tokenJWT import TokenData


class UserController:
    def __init__(self, userService: UserService = Depends()):
        self.userService = userService

    async def addPreference(self, current_user: TokenData, request: UserUpdateModel):
        try:
            # add user preference
            result = await self.userService.addPreference(current_user, request)
            return JSONResponse(
                status_code=200,
                content={
                    "message": "success add preference",
                    "preference": request.preference
                }
            )

        # jika terjadi error, tampilkan pesan error
        except Exception as e:
            return JSONResponse(
                status_code=500,
                content={
                    "message": "Error adding preference",
                    "error": str(e)
                }
            )
        
    async def addImageModel(self, current_user: TokenData, file_base64: AddRequestImageModel):
        try:
            # add user preference
            result = await self.userService.addImageModel(current_user, file_base64)
            return JSONResponse(
                status_code=200, message="success add image model")

        # jika terjadi error, tampilkan pesan error
        except Exception as e:
            return JSONResponse(
                status_code=500,
                content={
                    "message": "Error adding image model",
                    "error": str(e)
                }
            )
    
    async def getUserData(self, current_user: TokenData):
        try:
            # get user data
            result = await self.userService.getUserData(current_user)
            return JSONResponse(
                status_code=200,
                content={
                    "message": "success get user data",
                    "data": result
                }
            )

        # jika terjadi error, tampilkan pesan error
        except Exception as e:
            print(f"Error getting user: {e}")
            return JSONResponse(
                status_code=500,
                content={
                    "message": "Error getting user",
                    "error": str(e)
                }
            )
        