from abc import ABC, abstractmethod
from fastapi import UploadFile
import os
from typing import Optional

class BaseAudioTranscriber(ABC):
    """Abstract base class for plug-and-play audio transcription models."""

    @abstractmethod
    def load_model(self):
        """Load the transcription model (from disk, API, etc.)."""
        pass

    @abstractmethod
    async def transcribe(self, file: UploadFile) -> str:
        """Transcribe the given audio file and return text."""
        pass


# 🧠 Dummy Model (for now) — replace this later with your real model
class DummyAudioTranscriber(BaseAudioTranscriber):
    """A dummy placeholder that mimics a transcription process."""

    def __init__(self, model_path: Optional[str] = None):
        self.model_path = model_path
        self.model_loaded = False

    def load_model(self):
        """Pretend to load a model."""
        self.model_loaded = True
        print(f"[INFO] Dummy transcription model loaded from {self.model_path or 'default memory'}")

    async def transcribe(self, file: UploadFile) -> str:
        """Fake transcription: just returns a placeholder text."""
        if not self.model_loaded:
            self.load_model()

        # Optional: save file temporarily (useful if future models require a file path)
        temp_path = os.path.join("uploads", file.filename)
        os.makedirs("uploads", exist_ok=True)
        with open(temp_path, "wb") as f:
            f.write(await file.read())

        # 🔧 Replace this logic later with real model inference
        transcript = f"[Placeholder transcription for '{file.filename}']"

        # Optional cleanup
        # os.remove(temp_path)

        return transcript
