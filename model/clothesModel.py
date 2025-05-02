from typing import Optional
from pydantic import BaseModel


class ClothesModel(BaseModel):
    id: int
    type: str
    category: str
    color: str
    pattern: str
    length: str
    image_base64: str

class UpdateClothesModel(BaseModel):
    type: Optional[str] = None
    category: Optional[str] = None
    color: Optional[str] = None
    pattern: Optional[str] = None
    length: Optional[str] = None
    image_base64: Optional[str] = None


class ClothesRequestModel(BaseModel):
    type: str
    category: str
    color: str
    pattern: str
    length: str
    image_base64: str
    