from fastapi import Depends
from fastapi.responses import JSONResponse

from service.history.historyService import HistoryService
from utils.tokenJWT import TokenData


class HistoryController:
    def __init__(self, historyService: HistoryService = Depends()):
        self.historyService = historyService
    async def send_history(self, current_user : TokenData):
        try:
            data = await self.historyService.show_history(current_user)
            return {
                "message" : "Succesfuly",
                "data": data
            }
        except Exception as e:
            return JSONResponse(status_code=500, content={"Internal Server Error"})
        
