from fastapi import HTTPException
from utils.scrapingImage import scrape_dynamic


class VirtualTryOnService:
    def __init__(self ):
        pass

    async def scraping_image(self, url: str):
        try:
            # scraping image
            data = scrape_dynamic(url)

            # disini digunakan untuk promt image yang ada

            return data

        except Exception as e:
            return HTTPException(status_code=500, detail=str(e))

        