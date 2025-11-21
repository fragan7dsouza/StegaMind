from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.models.load_models import load_all
from backend.routers.detect import router as detect_router
from backend.routers.hide import router as hide_router
from backend.routers.extract import router as extract_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

load_all()

app.include_router(hide_router)
app.include_router(detect_router)
app.include_router(extract_router)

@app.get("/")
def root():
    return {"msg": "StegaMind API is running"}
