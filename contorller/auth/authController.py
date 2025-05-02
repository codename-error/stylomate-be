import logging
from fastapi import Depends, HTTPException
from fastapi.responses import JSONResponse
from model.userModel import UserLoginModel, UserRegisterModel
from service.auth.authService import AuthService


class AuthController:
    def __init__(self, authService: AuthService = Depends()):
        self.authService = authService

    async def loginEmailPassword(self, request: UserLoginModel):
        try:

            print("sebeleum memanggil login service")
            user_data = await self.authService.loginEmailPassword(request)
            
            print("masuk service")

            return JSONResponse(status_code=200, content={
                    "message": "User registered successfully",
                    "user": user_data
                })
        
        except HTTPException as e:
            return JSONResponse(status_code=400, content={"error": str(e)})
        
        except Exception as e:
            return JSONResponse(status_code=500, content={"error": "Internal Server error"})

    async def registerEmailPassword(self, request: UserRegisterModel):
        try:
            UserRegisterModel(**request.model_dump())
            user_data = await self.authService.registerEmailPassword(request)
            return JSONResponse(status_code=201, content={
                "message":"User Succesfuly Created",
                "data": user_data
            })
        except Exception as e:
            return JSONResponse(status_code=404, content={
                "error": "Validasi gagal", "details": str(e)
            } )
        
    async def sendCodeVerification(self, email: str):
        try:
            await self.authService.send_verification_code(email)
            return JSONResponse(status_code=200, content=f"Message Succesfuly send to {email}")
        except Exception as e:
            return JSONResponse(status_code=500, content=f"error: Send Email Failed {str(e)}")
    
    async def verifyEmailUser(self, email: str, code :int):
        try:
            await self.authService.verifyEmailOTP(email, code)
            return JSONResponse(status_code=200, content=f"Email Valid = {email}")
        except HTTPException as e:
            return JSONResponse(status_code=e.status_code, content={"error": e.detail})
        except Exception as e:
            return JSONResponse(status_code=500, content={"ERRROR"})

