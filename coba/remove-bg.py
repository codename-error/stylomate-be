async def createClotes(self,file : UploadFile, type: str,curent_user: TokenData):
        try:
            uid = curent_user.uid    

            logging.info(f"content-type: {file.content_type}") 
           
            output_path = './output.png'
            input = Image.open(file.file).convert("RGBA")
            output = remove(input)
            output.save(output_path)

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

            # ini adalah promt ke vertex ai
            if type == "top":
                promt =  os.getenv("PROMT_ATASAN")
            elif type == "bottom":
                promt = os.getenv("PROMT_BAWAHAN")
    
            # Single message
            img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")

            response = self.call_gpt(
                image_base64=img_str,
                text_prompt=promt
            )

            print(response)

            cleaned = response.replace("```json\n", "").replace("\n```", "")


            print(cleaned)


            # return await self.wardrobeRepository.add_clothes(uid, new_id, type, data["color"], data["sleeve_length"], data["neckline"], data["pattern"], img_str)

        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Failed To Add Clotest To wardrobe {str(e)}")