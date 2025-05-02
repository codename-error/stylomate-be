from fastapi import Depends, UploadFile
from fastapi.responses import JSONResponse
from model.clothesModel import ClothesRequestModel, UpdateClothesModel, UploadRequestModel
from service.wardrobe.wardrobeService import WadrobeService
from utils.tokenJWT import TokenData


class WardrobeController:
    def __init__(self, wardrobeService: WadrobeService = Depends()):
        self.wardrobeService = wardrobeService

    async def createClotes(self, request: UploadRequestModel,curent_user: TokenData):
        try:
            data_clothes = await self.wardrobeService.createClotes(request, curent_user)
            
            return JSONResponse(status_code=201, content={
                "message": "Succesfuly Created New Clothes",
                "data": data_clothes
            })

        except Exception as e:
            return JSONResponse(status_code=500, content={"message": "internal Server Error", "error": {str(e)}})
        
    async def getWardrobe(self, current_user: TokenData):
        try:
            data_wardrobe = await self.wardrobeService.getWardrobe(current_user)

            return JSONResponse(status_code=200,content={
                "message": "Succesfult Get Wardrobe item",
                "data": data_wardrobe
            })
        except Exception as e:
            return JSONResponse(status_code=500, content={"message": "Internal Server Error", "detail": {str(e)}})
        
    async def getClothesId(self, current_user: TokenData):
        try:
            data_clothes= await self.wardrobeService.getClothesId(current_user)

            return JSONResponse(status_code=200, content={
                "message": "Succesfuly get clothes by Id",
                "data": data_clothes
            })
        
        except Exception as e:
            return JSONResponse(status_code=500, content={"message": "Internal Server Error", "detail": {str(e)}})
        
    async def updateClothes(self, id: int , request: UpdateClothesModel, current_user: TokenData):
        try:
            
            data_update = await self.wardrobeService.updateClothes(id ,request, current_user)

            return JSONResponse(status_code=201, content={
                "message": "Update clothes succesfuly",
                "data_update": data_update
            })
        except Exception as e:
            error_detail = str(e) if not isinstance(e, set) else list(e)
            return JSONResponse(status_code=500, content={"message": "Internal Server Error", "detail": error_detail})
        
    async def deleteClothesById(self, id: int, current_user: TokenData):
        try:
            
            await self.wardrobeService.deleteClothesID(id, current_user)

            return JSONResponse(status_code=202, content=f"Succesfuly delete clothes id {id}")
        except Exception as e:
            return JSONResponse(status_code=400, content="Bad Request Failed delete")