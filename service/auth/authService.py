import json
import bcrypt
from fastapi import Depends
from firebase_admin import auth, storage
from model.userModel import UserLoginModel, UserModel, UserRegisterModel
from repository.auth.authRepository import AuthRepository
from fastapi import HTTPException
import smtplib
from email.message import EmailMessage

from utils.codeValidation import generateCode, verifyCode
from utils.generate_id import generateNewID
from utils.tokenJWT import create_acces_token
from utils.emailSender import send_verification_email
from utils.encripsiPassword import encripsi_password


class AuthService:
    def __init__(self, authRepository: AuthRepository = Depends()):
        self.authRepository = authRepository
        self.generateCode = generateCode
        self.verifyCode = verifyCode
        self.send_verificationOTP = send_verification_email
        self.encripsiPassword = encripsi_password

    async def loginEmailPassword(self, user_data: UserLoginModel):
        try:
            user = auth.get_user_by_email(user_data.email)
            # cek password

            data_user = await self.authRepository.getUserData(user.uid)
            
            if not data_user:
                raise HTTPException(status_code=404, detail="User not found")
            

            storage_password = data_user["password"]

            if isinstance(storage_password, bytes):
                storage_password = storage_password.decode('utf-8')
                
            if not bcrypt.checkpw(user_data.password.encode('utf-8'), storage_password.encode('utf-8')):
                    raise HTTPException(status_code=404, detail="Invalid Password")
            

            access_token = create_acces_token(
                data={"sub": user.uid}
            )

            return {"user": user.uid, "access_token": access_token, "token_type": "bearer"}
                
        except auth.UserNotFoundError:
            raise HTTPException(status_code=404, detail="User not found")

    async def registerEmailPassword(self, request: UserRegisterModel):
        try:
            passEncript = self.encripsiPassword(request.password)
            new_user = auth.create_user(email = request.email, password= request.password)

            new_id = generateNewID(request.email)
            
            user_data = {
                "id": new_id,
                "email": request.email,
                "username": request.username,
                "password": passEncript,
                "profile_picture": request.profile_picture or "",
                "preference": request.preference or [],
                "image_model": request.image_model or "",
            }

            user = UserModel(**user_data)
            access_token = create_acces_token(
                data={"sub": new_user.uid}
            )

            # add user to database
            await self.authRepository.addUserRegister(new_user.uid ,user)

            return {"user": new_user.uid, "access_token": access_token, "token_type": "bearer", "data": user_data}

        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Register Failed {str(e)}")
        
    async def verifyEmailOTP(self, email: str, code: int):
        try:
            # ceck code verification
            print("hallo agung")
            code_verified = await self.verifyCode(email, code)
            print(code_verified)
            if code_verified:
                return "Email Successfully Verified"
            else:
                raise HTTPException(status_code=400, detail="Invalid verification code")
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Register Failed: {str(e)}")

        
    async def send_verification_code(self,email: str):
        try:
            # generate code
            verification_code = self.generateCode(email)

            sender_email = "lemonodet1@gmail.com"

            self.send_verificationOTP(sender_email, email, verification_code)
            return "Berhasil"
        except Exception as e:
            return HTTPException(status_code=500, detail="Internal Server Eror, Gagal Mengirim Email")

            