from fastapi import Depends
from fastapi.responses import JSONResponse

from service.history.historyService import HistoryService


class HistoryController:
    def __init__(self, historyService: HistoryService = Depends()):
        self.historyService = historyService
    async def send_history(self, uid):
        try:
            data = await self.historyService.show_history(uid)
            return {
                "message" : "Succesfuly",
                "data": data
            }
        except Exception as e:
            return JSONResponse(status_code=500, content={"Internal Server Error"})
        
