from fastapi import Depends
from fastapi.responses import JSONResponse

from service.virtualtryon.virtualtryonService import VirtualTryOnService
from utils.tokenJWT import TokenData


class VirtualTryOnController:
    def __init__(self, virtualTryOnService: VirtualTryOnService = Depends()):
        self.virtualTryOnService = virtualTryOnService

    async def scraping_image(self, url: str):
        try:
            # scraping image
            data = await self.virtualTryOnService.scraping_image(url)

            # disini digunakan untuk promt image yang ada

            return JSONResponse(status_code=200,content={"message": "success", "data": data})

        except Exception as e:
            return JSONResponse(status_code=500, content={"message": "error", "detail": str(e)})