import base64
import json
from fastapi import Depends, HTTPException
from config.AzureConfig import  setup_gemini_chat
from model.clothesModel import UpdateClothesModel, UploadRequestModel
from repository.wardrobe.wardrobeRepository import WardrobeRepository
from utils.generate_id import generateNewID
from utils.tokenJWT import TokenData
from PIL import Image
from rembg import remove
from io import BytesIO
from langchain_core.messages import HumanMessage

class WadrobeService:
    def __init__(self, wardrobeRepository: WardrobeRepository = Depends(), gemini_config = Depends(setup_gemini_chat)):
        self.wardrobeRepository = wardrobeRepository
        self.gemini_config = gemini_config

    async def getWardrobe(self, current_user: TokenData):
        try:
            uid = current_user.uid
            return await self.wardrobeRepository.get_clothes(uid)
        
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Failed get wardrobe {str(e)}")
        
    async def createClotes(self, request: UploadRequestModel,curent_user: TokenData):
        try:
            uid = curent_user.uid    
            file = request.file

            image_data = base64.b64decode(file)
            # Open image using PIL
            input_image = Image.open(BytesIO(image_data)).convert("RGBA")
           
  
            output = remove(input_image)

            if output.mode != "RGBA":
                print("image not RGBA")
                output.convert("RGBA")
            
            new_id = generateNewID(uid)
            
            # menggunakan penyimpanan sementara
            buffered = BytesIO()
            output.save(buffered, format="PNG")
            # reset ke pointer 0
            buffered.seek(0)

            image_data = buffered.getvalue()

            img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")

            # ini adalah promt ke vertex ai
            promt = """**Analyze this clothing item image and provide detailed attributes in EXACTLY this JSON format:**
{
  "category": "Top/Bottom/Dress/Outerwear",
  "type": "T-Shirt/Blouse/Shirt/Sweater/Jeans/Skirt/Shorts/etc",
  "color": "Standard color name (e.g., Ivory White, Navy Blue, Jet Black)",
  "pattern": "Plain/Striped/Checkered/Floral/Graphic/Polka Dot/Abstract/etc",
  "length": "Crop/Waist/Hip/Midi/Maxi (for tops) or Short/Knee-Length/Ankle-Length (for bottoms)"
}

**Requirements:**
1. Be strictly consistent with the JSON structure and field names
2. Use only the specified values for each field:
   - Category: Top, Bottom, Dress, or Outerwear
   - Type: Specific garment type matching the category
   - Color: Standard color names (avoid vague descriptions)
   - Pattern: Clear pattern description or "Plain" if no pattern
   - Length: Appropriate length measurement for the category
3. If any attribute cannot be determined, use "Unknown"
4. Focus on the main clothing item in the image
5. Output ONLY raw JSON without markdown formatting
6. Ensure valid JSON syntax (double quotes, proper commas)

**Example valid response:**
{
  "category": "Top",
  "type": "Blouse",
  "color": "Ivory White",
  "pattern": "Small Flowers",
  "length": "Hip"
}"""

    
            # Single message
            # img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
            image_content = {"type": "image_url", "image_url": f"data:image/jpeg;base64,{img_str}"}

            message = HumanMessage(
                content=[
                    {'type': 'text', 'text': promt},
                    image_content
                ]
            )


            response = self.gemini_config.invoke([message])
            cleaned = response.content.replace("```json\n", "").replace("\n```", "")

            data = json.loads(cleaned)


            return await self.wardrobeRepository.add_clothes(uid, new_id, data["type"], data["color"], data["length"], data["category"], data["pattern"], img_str)

        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Failed To Add Clotest To wardrobe {str(e)}")
        
    async def getClothesId(self ,current_user: TokenData):
        try:
            uid = current_user.uid

            return await self.wardrobeRepository.get_clothes_by_id(uid)

        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Error to get data by id from wardrobe{str(e)}")

    async def deleteClothesID(self, id: int, current_user: TokenData):
        try:
            uid = current_user.uid

            return await self.wardrobeRepository.delete_clothes(uid, id)
        
        except Exception as e:
            raise HTTPException(status_code=500, detail={str(e)})
    
    async def updateClothes(self ,id: int ,request: UpdateClothesModel, current_user: TokenData ):
        try:
            uid = current_user.uid

            return await self.wardrobeRepository.update_clothes(id ,request, uid)

        except Exception as e:
            raise HTTPException(status_code=500, detail={str(e)})
