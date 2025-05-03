from pydantic import BaseModel


class HistoryModel(BaseModel):
    fitur: str
    tanggal: str
    point: str