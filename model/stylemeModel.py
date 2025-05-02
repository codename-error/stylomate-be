from pydantic import BaseModel


class StyleMeRequest(BaseModel):
    id: int
    kondisi: str
    activity: str