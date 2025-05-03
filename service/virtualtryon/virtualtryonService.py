from io import BytesIO
from fastapi import Depends, HTTPException
from repository.history.historyRepository import HistoryRepository
from repository.user.userRepository import UserRepository
from repository.wardrobe.wardrobeRepository import WardrobeRepository
import requests

from utils.tokenJWT import TokenData


class VirtualTryOnService:
    def __init__(self, wardrobeRepository: WardrobeRepository = Depends(), userRepository: UserRepository = Depends(), historyRepository: HistoryRepository= Depends() ):
        self.wardrobeRepository = wardrobeRepository
        self.userRepository = userRepository
        self.historyRepositroy = historyRepository

    async def scraping_image(self, current_user: TokenData, url: str):
        try:
            uid = current_user.uid
            # scraping image

            # response = requests.get(data["images"], stream=True)
            # response.raise_for_status()

            # # Simpan gambar ke BytesIO
            # image_bytes = BytesIO()
            # for chunk in response.iter_content(1024):
            #     image_bytes.write(chunk)
            feature = "styleMe"
            ponit = 5

            await self.userRepository.update_coint(uid)
            await self.historyRepositroy.save_history(feature, ponit, uid )
            


            # disini digunakan untuk promt image yang ada

        except Exception as e:
            return HTTPException(status_code=500, detail=str(e))
    
    async def download_image(self, url, save_path):
        try:
            response = requests.get(url, stream=True)
            response.raise_for_status()

            with open(save_path, 'wb') as file:
                for chunk in response.iter_content(1024):
                    file.write(chunk)

            print("gambar bergask disimpan ")
        
        except Exception as e:
            print(e)
            return False
        
    async def get_image(self, current_user: TokenData):
        try:
            uid = current_user.uid


            data = self.wardrobeRepository.get_clothes(uid)

            return data
        except Exception as e:
            return False
        
    async def send_image_to_model(self, current_user: TokenData):
        try:
            uid = current_user.uid

            # login untuk send image to model
        
        except Exception as e:
            print(e)


        