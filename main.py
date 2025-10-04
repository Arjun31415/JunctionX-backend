# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.audio import router as audio_router

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or specify your frontend origin like ["http://localhost:3000"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(audio_router)

@app.get("/")
async def root():
    return {"message": "Hello, World!"}