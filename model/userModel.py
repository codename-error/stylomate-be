from typing import Optional
from pydantic import BaseModel, Field, field_validator, ValidationInfo


class UserModel(BaseModel):
    id: int
    username: str
    email: str
    password: str
    coint: int
    profile_picture: Optional[str] = None
    preference: Optional[list[str]] = None
    image_model: Optional[str] = None

class UserLoginModel(BaseModel):
    email: str
    password: str

class UserRegisterModel(BaseModel):
    username: str = Field(..., title="Username")
    email: str = Field(..., title="Email")
    password: str = Field(..., title="Password")
    validate_password: str = Field(..., title="Validate Password")
    profile_picture: Optional[str] = None
    preference: Optional[list[str]] = None
    image_model: Optional[str] = None


    @field_validator("password")
    def validate_password(cls, value):
        if len(value) < 8:
            raise ValueError("Password must be at least 8 characters long")
        if not any(char.isdigit() for char in value):
            raise ValueError("Password must contain at least one digit")
        if not any(char.isalpha() for char in value):
            raise ValueError("Password must contain at least one letter")
        
        return value
    
    def validate_confirm_password(cls, value: str, values: ValidationInfo):
        if "password" not in values.data:
            raise ValueError("Password field is required")
        password = values.data["password"]
        if value != password:
            raise ValueError("Passwords do not match")
        return value
    
class UserUpdateModel(BaseModel):
    username: Optional[str] = None
    profile_picture: Optional[str] = None
    preference: Optional[list[str]] = None
    image_model: Optional[str] = None