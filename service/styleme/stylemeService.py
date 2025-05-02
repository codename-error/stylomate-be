
import base64
import io
import json
import random
from typing import Optional
from fastapi import Depends, HTTPException, UploadFile
from google.genai import types
from config.AzureConfig import setup_gemini_chat
from config.azureCon import setup_openai_chat
from repository.user.userRepository import UserRepository
from repository.wardrobe.wardrobeRepository import WardrobeRepository
from utils.promtText import styleme
from utils.tokenJWT import TokenData
from datetime import datetime
from langchain_core.messages import HumanMessage

class StyleMeService:
    def __init__(self, wardrobeRepository: WardrobeRepository = Depends(), userRepository: UserRepository = Depends(), client_open_ai = Depends(setup_gemini_chat)):
        self.wardrobeRepository = wardrobeRepository
        self.userRepository = userRepository
        self.client_open_ai = client_open_ai
        self.styleme = styleme

    async def generateRekomendasi(self, id : Optional[int], cari: str,  activity: str,current_user: TokenData):
        try:     
            uid = current_user.uid
            print("masuk sini ")
            # Ambil data pakaian dari wardrobe
            data_rekomendasi = await self.wardrobeRepository.get_clothes_whitout_image(uid)
            # Kelompokkan berdasarkan kategori
            top_clothes = [item for item in data_rekomendasi if item.get("category") == "Top"]
            bottom_clothes = [item for item in data_rekomendasi if item.get("category") == "Bottom"]
                

            if not data_rekomendasi:
                return {"message": "Wardrobe is empty"}
            
            # ambil waktu sekarang
            waktu_sekarang = datetime.now()

            print("waktu sekarang", waktu_sekarang)
            # get preference user
            preference = await self.userRepository.get_preference(uid)
            print("preference", preference)
            if not preference:
                return {"message": "Wardrobe is empty"}
            
            if cari != "None":
                if cari == "Top":
                    kondisi = "Bottom"
                    data = bottom_clothes
                elif cari == "Bottom":
                    kondisi = "Top"
                    data = top_clothes


                data_baju_user = await self.wardrobeRepository.get_clothes_witout_image(uid, id)
                if not data_baju_user:
                    return {"message": "Wardrobe is empty"}

                print("data baju user", data_baju_user)
            
            
                promt  = f"""You are an AI fashion stylist. Given a {kondisi} item and a list of available {kondisi} items (with unique IDs), recommend the most suitable {kondisi} by returning only the ID of the best-matching item.
                Input Format:
                {kondisi} item:
                {data_baju_user}
                {cari} items:
                {data}
                // Add more bottoms with unique IDs
                ]
                User Preferences: 
                {preference}
                Context:
                {
                waktu_sekarang,
                activity
                }

                Output Format (only valid JSON, no markdown):

                recommendation:

                "id": "{kondisi} id IN NUMBER NOT STRING",

                INTEGER NOT STRING

                note:

                dont use id in data_baju_user


                Guidelines:
                - Choose the best-matching bottom based on type, color, pattern, and length harmony with the top. 
                - Alignment with style_preference (highest priority — must reflect the user’s fashion style)
                - Consider the occasion and color preference as secondary factors.
                - Do not include explanation—only return the ID.
                - Use only the id field from the matching item as output.
                - Output must be valid JSON with double quotes."""
            

            # recomendation using vertex ai
            else:
                promt = f"""You are an AI fashion stylist. Given a list of top items and a list of bottom items (each with unique IDs), recommend the best combination (top + bottom) that matches well based on style, color, pattern, length harmony, and user preferences.
                Input Format:
                Available tops:
                [
                {top_clothes}
                // Add more tops
                ]
                Available bottoms:
                [
                {bottom_clothes}
        
                // Add more bottoms
                ]
                User Preferences:
                {preference}
                Context:
                {
                waktu_sekarang,
                activity
                }
                Output Format (only valid JSON, no markdown):

                "recommended_combination": 
                "top_id": "1",
                "bottom_id": "2"

                make sure to use id in data_baju_user and id is in number not string
            
                Guidelines:
                - Evaluate all possible top-bottom pairings.
                - Prioritize alignment with style_preference (must match user’s style).
                - Ensure visual harmony in color, pattern, and length.
                - Consider suitability for the given occasion.
                - Return only the best combination.
                - Do not include explanation—only output the selected IDs.
                - Output must be valid JSON with double quotes."""

            message = HumanMessage(
                content=[
                    {'type': 'text', 'text': promt},
                ]
            )


            response = self.client_open_ai.invoke([message])
            cleaned = response.content.replace("```json\n", "").replace("\n```", "")

            data = json.loads(cleaned)
            print("data", data)

            # hasil_rekomendasi = await self.wardrobeRepository.get_clothes_by_id(uid, id)
            # if not hasil_rekomendasi:
            #     return {"message": "Wardrobe is empty"}

            # return {
            #     "message": "success",
            #     "data": hasil_rekomendasi
            # }
            return True
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Failed to generate rekomendasi {str(e)}")
        
    async def getWardrobe(self, userId: str):
        try:
            # Ambil data pakaian dari wardrobe
            clothes = await self.wardrobeRepository.get_clothes(userId)
            if not clothes:
                return {"message": "Wardrobe is empty"}
            
            return {
                "message": "success",
                "data": clothes
            }
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Failed to get wardrobe {str(e)}")

    async def getItem(self, itemId: int, userId: TokenData,):
        try:
            uid = userId.uid

            # Ambil data pakaian dari wardrobe
            clothes = await self.wardrobeRepository.get_clothes_by_id(uid, itemId)
            if not clothes:
                return {"message": "Wardrobe is empty"}
            
            return {
                "message": "success",
                "data": clothes
            }
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Failed to get item {str(e)}")
        
    async def get_item_by_category(self, category : str, curent_user: TokenData):
        try:
            uid = curent_user.uid
            # Ambil data pakaian dari wardrobe
            clothes = await self.wardrobeRepository.get_clothes_by_category(uid, category )
            
            print("masuk sini")

            if not clothes:
                return {"message": "Wardrobe is empty"}
            
            return {
                "message": "success",
                "data": clothes
            }
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Failed to get item {str(e)}")
    
    async def generateRandom(self, userId: TokenData, cari: str):
        try:
            uid = userId.uid

            # Ambil data pakaian dari wardrobe
            clothes = await self.wardrobeRepository.get_clothes(uid)
            if not clothes:
                return {"message": "Wardrobe is empty"}

            # Kelompokkan berdasarkan kategori
            top_clothes = [item for item in clothes if item.get("category") == "Top"]
            bottom_clothes = [item for item in clothes if item.get("category") == "Bottom"]

            # Cek apakah masing-masing kategori punya item
            if not top_clothes or not bottom_clothes:
                return {"message": "Wardrobe must contain both 'top' and 'bottom' items"}

            # Ambil satu item secara acak dari masing-masing kategori
            selected_top = random.choice(top_clothes)
            selected_bottom = random.choice(bottom_clothes)

            if cari == "Top":
                selected = selected_top
            elif cari == "Bottom":
                selected = selected_bottom
            else:
                selected = {"Top": selected_top, "Bottom": selected_bottom}



            return {
                "message": "success",
                "data": selected
            }
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Failed to get item {str(e)}")
            

