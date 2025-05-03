# BACKEND STYLOMATE DOCUMENTATION

# Arsitektur Code

Dalam Arsitektur yang dibangun untuk membangun sebuah backend aplikasi stylomate menggunakan MVC (Model View Controller), dengan pendekatan clean code arsitektur dan juga monolitic berikut adalah code bagian backend dari aplikasi staylo mate:

```json
- config
- controller
- repository
- service
- model
- router
main.py
.env
```

# Instalation and Implementation

Hal yang perlu dilakukan untuk menjalankan code ini pastikan instalasi python di laptop atau komputer anda. berikut adalah langkah pertama:

```json
git clone https://github.com/codename-error/stylomate-be.git
```

Selanjutnya ke dalam direktory yang sudah di tentukan

```json
cd stylemate-be
```

selanjutnya adalah melakukan instalasi package

```json
pip install -t requirements.txt
```

selanjutnya adalah menjalankan dengan menjalankan berikut di terminal anda:

```json
uvicorn main:app --reload
```

setelah berhasil maka port default dari project ini adalah 8000

# Enpoint RestAPI

URI = http://localhost:8000/

diikuti dengan Enpoint setelahnya, contoh = http://localhost:8000/v2/login

# Login

**End Poin :** /v2/login

Methode : POST

Request:

```json
{
  "email": "string",
  "password": "string"
}
```

Response:

- 200 → OK

```json
{
  "message": "User registered successfully",
  "user": {
    "user": "",
    "access_token": ""
    "token_type": "bearer"
  }
}
```

- 500 → Internal Server Error

# Register

Endpoint: /v2/register

Methode : POST

request Body:

```json
{
  "username": "string",
  "email": "string",
  "password": "string",
  "validate_password": "string",
  "profile_picture": "string",
  "preference": [
    "string"
  ],
  "image_model": "string"
}
```

response Body:

- 200 → OK

```json
{
  "message": "User registered successfully",
  "user": {
    "user": "",
    "access_token": ""
    "token_type": "bearer"
  }
}

```

- 500 → Internal Server Error

# Preference

Endpoint: /v2/user/preference

Methode: PUT

request Body:

```json
{
  "username": "string",
  "profile_picture": "string",
  "preference": [
    "string"
  ],
  "image_model": "string"
}
```

response Body:

- 201 → Created
- 400 → internal server error

# Image Model

Endpoint : /v2/user/image_model

Methode: PUT

request_body:

```json
from-data
file *string($binary)
```

Response Body:

- 201 Created
- 400 Not Found

# Wardrobe

### 1. Get wardrobe

     End point: /wardrobe

method: GET

Response:

```json
{    "message": "Succesfult Get Wardrobe item",    
	"data": [
		{"type": "T-Shirt",
		"length": "Hip",
		"id": 1,
		"category": "Top",
		"image_url":base64,
		"color": "White",           
		"pattern": "Plain"}
]
}
```

### 2. Update Wardrobe

method: PUT

params:

```json
/id → wardobe/1
```

body:

```json
class UpdateClothesModel(BaseModel):
type: Optional[str] = None
category: Optional[str] = None
color: Optional[str] = None
pattern: Optional[str] = None
length: Optional[str] = None
image_base64: Optional[str] = None
```

Response:
202 → No Conten

### 3. Delete Wardrobe

     methode: DELETE

params:

```json
/id → wardobe/1
```

Response:

202 → No Content

### 4. Create Clothes

     methode: POST

body:

```json
multipart/form data: file image (jpg/png)
```

response:

201 → created

# Style Me

### 1. Recomendation

     Endpoint : /v2/recomendation

Methode: POST

Request Body:

```json
{
  "id": 0,
  "kondisi": "string",
  "activity": "string"
}
```

Response:

- 200 → OK
- 400 → Not Found

### 2. Styleme for category

     Endpoint : /v2/styleme/category

Methode : GET

Request Body:

```json

{
  "category": "string"
}

input = ["Top"/ "Bottom"]
```

Response Body:

- 200 → Oke
- 500 → Internal Server Error

### 3. Style Me random

     Endpoint : /v2/styleme/random

Methode: GET

Request Body:

```json
{
  "cari": "string"
}

input = ["Top" / "Bottom" / "None"]
```

Response Body:

- 200 → Ok
- 500 → Internal Server error

### 4. Get Item Style By Id

     Endpoint : /v2/styleme/{id}

Methode: GET

Parameters:

```json
id = ....(int)
```

Response Body

- 200 → Ok
- 500 → Internal Server Error

# Stylo Ai

### 1. Upload Link

     Endpoint : /v2/url

Methode: GET

Request Body:

```json
Form Data 
```

Response Body:

- 200 → OK
- 500 → Internal Server Error

### 2. Get Wardrobe

      Endpoint : /v2/stylo/wardrobe

Methode: GET

response Body:

```json
{    "message": "Succesfult Get Wardrobe item",    
	"data": [
		{"type": "T-Shirt",
		"length": "Hip",
		"id": 1,
		"category": "Top",
		"image_url":base64,
		"color": "White",           
		"pattern": "Plain"}
]
}
```

### 3. Generate AI

     Endpoint: /v2/styloai

Methode: POST

Request Body:

```json
{
	"image": base64,
	"image": base64
}
```

response Body:

     

```json
hasilnya image
```