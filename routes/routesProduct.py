from fastapi import APIRouter, Depends, Form, UploadFile
from contorller.auth.authController import AuthController
from contorller.wardrobe.wardrobeController import WardrobeController
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



# ------- wardrobe ------- #

# --------- wardrobe ---------------

@router.get("/wardrobe")
async def getWardrobe(current_user: TokenData = Depends(get_current_user), wardrobeController: WardrobeController = Depends()):
    return await wardrobeController.getWardrobe(current_user)

@router.get("/wardrobe/{id}")
async def getWardrobeId(current_user: TokenData = Depends(get_current_user), wardrobeController: WardrobeController =Depends()):
    return await wardrobeController.getClothesId(current_user)

@router.post("/wardrobe/create")
async def createClothes(file: UploadFile, type: str = Form(...), current_user: TokenData = Depends(get_current_user), wardrobeController: WardrobeController = Depends()):
    return await wardrobeController.createClotes(file, type, current_user)

@router.put("/wardrobe/{id}")
async def updateClothes(id: int ,request: UpdateClothesModel, current_user: TokenData = Depends(get_current_user), wardrobeController: WardrobeController = Depends()):
    return await wardrobeController.updateClothes(id, request, current_user)

@router.delete("/wardrobe/{id}")
async def deleteClothes(id: int, current_user: TokenData = Depends(get_current_user), wardrobeController: WardrobeController = Depends()):
    return await wardrobeController.deleteClothesById(id, current_user)
