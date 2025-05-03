
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

            # Ambil data pakaian dari wardrobe
            data_rekomendasi = await self.wardrobeRepository.get_clothes_whitout_image(uid)
            # Kelompokkan berdasarkan kategori
            top_clothes = [item for item in data_rekomendasi if item.get("category") == "Top"]
            bottom_clothes = [item for item in data_rekomendasi if item.get("category") == "Bottom"]
            

            if not data_rekomendasi:
                return {"message": "Wardrobe is empty"}
            
            # ambil waktu sekarang
            waktu_sekarang = datetime.now()

            # get preference user
            preference = await self.userRepository.get_preference(uid)
            if not preference:
                return {"message": "Wardrobe is empty"}
            
            if cari != "None":


                data_baju_user = await self.wardrobeRepository.get_clothes_witout_image(uid, id)
                if not data_baju_user:
                    return {"message": "Wardrobe is empty"}
                
                if cari == "Top":
                    promt = f"""rekomendasi baju
                    You are an AI fashion stylist. Given a bottom item and a list of available top items (with unique IDs), recommend the most suitable top by returning only the ID of the best-matching item.
                    Input Format:
                    Bottom item:
                    {data_baju_user}
                    Available tops:
                    [
                    {top_clothes}
                    // Add more tops with unique IDs
                    ]
                    User Preferences:
                    {preference}
                    Context:
                    {waktu_sekarang}
                    Output Format (only valid JSON, no markdown):
                    
                    "recommended_top_id": "1" 
                    
                    make sure to use id in data_baju_user and id is in number not string
                    pastikan {data_baju_user} tidak sama dengan {top_clothes}
                    pastikan bahwa cocok jika dikombinasikan, jadi makesure bahwa yang direkomendasikan itu benar22cocok sekali
                    
                    Guidelines:
                    - Choose the best-matching top based on type, color, pattern, and length harmony with the bottom.
                    - Prioritize alignment with style_preference (must reflect the user’s fashion style).
                    - Consider the occasion and color preference as secondary factors.
                    - Do not include explanation—only return the ID.
                    - Output must be valid JSON with double quotes."""
                elif cari == "Bottom":
                    promt = f"""You are an AI fashion stylist. Given a top item and a list of available bottom items (with unique IDs), recommend the most suitable bottom by returning only the ID of the best-matching item.
                    Input Format:
                    Top item:
                    {data_baju_user}
                    Available bottoms:
                    [
                    {bottom_clothes}
                    // Add more bottoms with unique IDs
                    ]
                    User Preferences: 
                    {preference}
                    Context:
                    {waktu_sekarang}
                    Activity: {activity}

                    Output Format (only valid JSON, no markdown):
                    
                    "recommended_bottom_id": "1"
                    make sure to use id in data_baju_user and id is in number not string
                    pastikan {data_baju_user} tidak sama dengan {bottom_clothes}
                    pastikan bahwa cocok jika dikombinasikan, jadi makesure bahwa yang direkomendasikan itu benar22cocok sekali

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
                pastikan  tidak sama dengan {top_clothes} dan {bottom_clothes}
                dan berikan rekomendasi baju dan celana jangan salah satu
                pastikan bahwa cocok jika dikombinasikan, jadi makesure bahwa yang direkomendasikan itu benar22cocok sekali
                
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
            result = {}

            if cari == "Top":
                recommendation = data.get("recommended_top_id")
                if recommendation:
                    top_item = await self.wardrobeRepository.get_clothes_by_id(uid, recommendation)
                    if top_item:
                        result["top"] = top_item
            elif cari == "Bottom":
                recommendation = data.get("recommended_bottom_id")
                if recommendation:
                    bottom_item = await self.wardrobeRepository.get_clothes_by_id(uid, recommendation)
                    if bottom_item:
                        result["bottom"] = bottom_item
            else:
                recommendation = data.get("recommended_combination")
                print(recommendation)
                if recommendation:
                    top_item = await self.wardrobeRepository.get_clothes_by_id(uid, recommendation.get("top_id"))
                    if top_item:
                        result["top"] = top_item

                    bottom_item = await self.wardrobeRepository.get_clothes_by_id(uid, recommendation.get("bottom_id"))
                    if bottom_item:
                        result["bottom"] = bottom_item
            if not result:
                return {"message": "Wardrobe is empty"}
            
            # mengurangi point user karena menggunakan feature berbayar
            self.userRepository.update_coint(uid)

            return {
                "message": "success",
                "data": result
            }
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
            

