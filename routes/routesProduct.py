from fastapi import APIRouter, Depends, Form, UploadFile
from contorller.auth.authController import AuthController
from model.clothesModel import ClothesRequestModel, UpdateClothesModel
from model.userModel import UserLoginModel, UserRegisterModel, UserUpdateModel
from utils.tokenJWT import TokenData, create_acces_token, get_current_user


# digunakan untuk testing v1
router = APIRouter(prefix="/v2")

@router.post("/login")
async def loginEmailPassword(request: UserLoginModel, authController: AuthController = Depends()):
    return await authController.loginEmailPassword(request)

@router.post("/register")
async def registerEmailPassword(request: UserRegisterModel, authController: AuthController = Depends()):
    return await authController.registerEmailPassword(request)

@router.post("/sendOTP")
async def sendCodeOTP(email: str, authController : AuthController = Depends()):
    return await authController.sendCodeVerification(email)


@router.post("/verify")
async def verifyEmail(email: str, code: int, authController : AuthController = Depends()):
    return await authController.verifyEmailUser(email, code)


