from fastapi import Depends
from repository.history.historyRepository import HistoryRepository
from utils.tokenJWT import TokenData


class HistoryService:
    def __init__(self, historyRepository: HistoryRepository = Depends()):
        self.historyRepository = historyRepository

    async def show_history(self, current_user: TokenData):
        try:
            uid = current_user.uid

            data = await self.historyRepository.get_history(uid)

            return data

        except Exception as e:
            return False