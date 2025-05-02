from fastapi import Depends
from repository.user.userRepository import UserRepository
from repository.wardrobe.wardrobeRepository import WardrobeRepository


class StyleMeRepository:
    def __init__(self, db : WardrobeRepository = Depends(), userRepository: UserRepository = Depends()):
        self.wardrobeRepository = db
        self.userRepository = userRepository

    async def getWardrobe(self, userId: str):
        return await self.wardrobeRepository.get_clothes(userId)
    
    async def getItem(self, userId: str, itemId: int):
        return await self.wardrobeRepository.get_clothes_by_id(userId, itemId)

    async def getPreference(self, userId: str):
        data = await self.userRepository.getUserData(userId)

        for key, value in data.items():
            if key == "preference":
                return value
    
    