# mendaftarkan api router v1
from fastapi import FastAPI
from routes.routesProduct import router as v2
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI



app = FastAPI()

# menambahkan middleware CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# menambahkan api router v1
app.include_router(v2)