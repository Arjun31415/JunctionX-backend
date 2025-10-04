from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from services.audio_service import handle_audio_upload
import os

router = APIRouter(prefix="/audio", tags=["Audio"])

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/transcribe")
async def transcribe_audio(file: UploadFile = File(...)):
    return await handle_audio_upload(file)
