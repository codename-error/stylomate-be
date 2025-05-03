from typing import Optional
from fastapi import Depends
from model.clothesModel import CategoryRequestModel, RandomRequestModel
from model.stylemeModel import StyleMeRequest
from service.styleme.stylemeService import StyleMeService
from utils.tokenJWT import TokenData


class StyleMeController:
    def __init__(self, styleMeService: StyleMeService  = Depends()):
        self.styleMeService = styleMeService

    async def generateRekomendasi(self, request: StyleMeRequest, current_user: TokenData):
        try:
            rekomendasi = await self.styleMeService.generateRekomendasi(request.id, request.cari, request.activity, current_user)
            return {
                "status": "success",
                "data": rekomendasi
            }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e)
            }
        
    async def getClothesByCategory(self, category: CategoryRequestModel, current_user: TokenData):
        try:
            clothes = await self.styleMeService.get_item_by_category(category.category, current_user)
            return {
                "status": "success",
                "data": clothes
            }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e)
            }

    async def getClothesById(self, id: int, current_user: TokenData):
        try:

            clothes = await self.styleMeService.getItem(id, current_user)
            return {
                "status": "success",
                "data": clothes
            }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e)
            }
        
    async def generateRandom(self, current_user: TokenData, cari: RandomRequestModel):
        try:
            clothes = await self.styleMeService.generateRandom(current_user, cari.cari)
            return {
                "status": "success",
                "data": clothes
            }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e)
            }