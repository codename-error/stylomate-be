from pydantic import BaseModel


class StyleMeRequest(BaseModel):
    id: int
    cari: str
    activity: str