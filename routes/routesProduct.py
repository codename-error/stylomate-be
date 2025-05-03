from fastapi import APIRouter, Depends, Form, UploadFile
from controller.auth.authController import AuthController
from controller.styleme.stylemeController import StyleMeController
from controller.user.userController import UserController
from controller.virtualtryon.virtaltryonController import VirtualTryOnController
from controller.wardrobe.wardrobeController import WardrobeController
from model.clothesModel import CategoryRequestModel, ClothesRequestModel, RandomRequestModel, UpdateClothesModel, UploadRequestModel
from model.stylemeModel import StyleMeRequest
from model.userModel import AddRequestImageModel, UserLoginModel, UserRegisterModel, UserUpdateModel
from repository.user.userRepository import UserRepository
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


# ------- users ---------
@router.put("/user/preference")
async def add_preference(request: UserUpdateModel ,current_user: TokenData = Depends(get_current_user), userController: UserController = Depends()):
    return await userController.addPreference(current_user, request)

@router.put("/user/image_model")
async def addImageModel(file_base64: AddRequestImageModel,current_user: TokenData = Depends(get_current_user), userController: UserController = Depends()):
    return await userController.addImageModel(current_user, file_base64)


# --------- wardrobe ---------------

@router.get("/wardrobe")
async def getWardrobe(current_user: TokenData = Depends(get_current_user), wardrobeController: WardrobeController = Depends()):
    return await wardrobeController.getWardrobe(current_user)

@router.get("/wardrobe/{id}")
async def getWardrobeId(current_user: TokenData = Depends(get_current_user), wardrobeController: WardrobeController =Depends()):
    return await wardrobeController.getClothesId(current_user)

@router.post("/wardrobe/create")
async def createClothes(request : UploadRequestModel, current_user: TokenData = Depends(get_current_user), wardrobeController: WardrobeController = Depends()):
    return await wardrobeController.createClotes(request, current_user)

@router.put("/wardrobe/{id}")
async def updateClothes(id: int ,request: UpdateClothesModel, current_user: TokenData = Depends(get_current_user), wardrobeController: WardrobeController = Depends()):
    return await wardrobeController.updateClothes(id, request, current_user)

@router.delete("/wardrobe/{id}")
async def deleteClothes(id: int, current_user: TokenData = Depends(get_current_user), wardrobeController: WardrobeController = Depends()):
    return await wardrobeController.deleteClothesById(id, current_user)


# -------- styleme ---------

@router.post("/recomendation")
async def generateRekomendasi(request: StyleMeRequest, current_user: TokenData = Depends(get_current_user), styleMeController: StyleMeController = Depends()):
    return await styleMeController.generateRekomendasi(request, current_user)

@router.get("/styleme/category")
async def getClothesByCategory(category: CategoryRequestModel, current_user: TokenData = Depends(get_current_user), styleMeController: StyleMeController = Depends()):
    return await styleMeController.getClothesByCategory(category, current_user)

@router.get("/styleme/random")
async def generateRandom(cari: RandomRequestModel,current_user: TokenData = Depends(get_current_user), styleMeController: StyleMeController = Depends()):
    return await styleMeController.generateRandom(current_user, cari)

@router.get("/styleme/{id}")
async def getClothesById(id: int, current_user: TokenData = Depends(get_current_user), styleMeController: StyleMeController = Depends()):
    return await styleMeController.getClothesById(id, current_user)



#  ------- virtual try on ---------
@router.get("/url")
async def scraping_image(
    url: str = Form(...), 
    current_user: TokenData = Depends(get_current_user),
    virtualTryOnController: VirtualTryOnController = Depends()):
    
    return await virtualTryOnController.scraping_image(current_user, url)








@router.get("/ping")
async def ping():
    access_token = create_acces_token(
                data={"sub": "Nis2yCgGXsZQSmbV73pz7rYpI9E2"}
            )
    return {"message": access_token}

@router.get("/pong")
async def userData(userRepository: UserRepository = Depends(), current_user: TokenData = Depends(get_current_user)):

    uid = current_user.uid

    Data = await userRepository.getUserData(uid)
    print(Data)
    if Data is None:
        return {"message": "User not found"}
    return {"message": Data}