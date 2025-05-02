# Documentasi testing

---

```
# 📘 StyloMate API Documentation (v1)

This document provides an overview of the testing API endpoints available in the StyloMate backend.

---

## ✅ Base URL
```

/v1 = contoh [http://127.0.0.1:8000/v1/wardrobe](http://127.0.0.1:8000/v1/wardrobe)

```
---

## 📂 Authentication

### 🔐 Login

**Endpoint**: `/login`
**Method**: `POST`
**Request Body**:
```json
{
  "email": "test",
  "password": "test"
}
```

**Response**:

```
{ "message": "Login successful" }
```

---

### **Register**

**Endpoint**: /register

**Method**: POST

**Request Body**:

```
{
  "email": "test",
  "password": "test"
}
```

**Response**:

```
{ "message": "Register successful" }
```

---

## **Wardrobe Management**

### **Get All Wardrobe Items**

**Endpoint**: /wardrobe

**Method**: GET

**Response**:

```
{
  "message": "Wardrobe data retrieved successfully",
  "data": [ ... ]
}
```

---

### **Get Item by ID**

**Endpoint**: /wardrobe/{clothes_id}

**Method**: GET

**Response (success)**:

```
{
  "message": "Wardrobe data retrieved successfully",
  "data": { ... }
}
```

---

### **Delete Item by ID**

**Endpoint**: /wardrobe/delete

**Method**: POST

**Query Param**:

```
clothes_id=<string>
```

**Response**:

```
{ "message": "Wardrobe data deleted successfully" }
```

---

### **Update Item**

**Endpoint**: /wardrobe/update

**Method**: POST

**Query Param**:

```
clothes_id=<string>
```

**Body**:

```
{
  "name": "New Name",
  "size": "L"
}
```

**Response**:

```
{ "message": "Wardrobe data updated successfully" }
```

---

## **AI-Powered Features**

### **Style Matching**

**Endpoint**: /style-match

**Method**: POST

**Request Body**:

```
{
  "color": "white",
  "style": "casual"
}
```

**Response**:

```
{
  "message": "Recommended outfits based on style preferences",
  "data": [ ... ]
}
```

---

### **Virtual Try-On (Save Result)**

**Endpoint**: /try-on/save

**Method**: POST

**Query Params**:

```
user_id=<string>&image_url=<string>
```

**Response**:

```
{
  "message": "Virtual try-on image saved successfully",
  "preview": "https://example.com/image.jpg"
}
```

---

### **Custom Clothing Design**

**Endpoint**: /design/custom

**Method**: POST

**Request Body**:

```
{
  "color": "red",
  "pattern": "striped",
  "size": "M"
}
```

**Response**:

```
{
  "message": "Custom design created successfully",
  "preview": "https://example.com/custom_design.jpg"
}
```

---

## **Personalization**

### **Set Style Preferences**

**Endpoint**: /preferences/style

**Method**: POST

**Request Body**:

```
{
  "style": "smart casual",
  "color": "blue"
}
```

**Response**:

```
{ "message": "Style preferences saved" }
```

---

### **Get Style Recommendations**

**Endpoint**: /recommendations/style/{user_id}

**Method**: GET

**Response**:

```
{
  "message": "Style recommendations for user {user_id}",
  "data": [ ... ]
}
```

---

## **Health Check**

### **Root**

**Endpoint**: /

**Method**: GET

**Response**:

```
{ "Hello": "World" }
```

---