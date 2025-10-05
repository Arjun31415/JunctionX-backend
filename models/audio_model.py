from abc import ABC, abstractmethod
from fastapi import UploadFile
import torch
import os
from typing import Optional


class BaseAudioTranscriber(ABC):
    """Abstract base class for all audio transcription models."""

    @abstractmethod
    def load_model(self):
        """Load the transcription model (from disk, API, etc.)."""
        pass

    @abstractmethod
    async def transcribe(self, file: UploadFile) -> str:
        """Transcribe the given audio file and return the text."""
        pass

class WhisperXTranscriber(BaseAudioTranscriber):
    def __init__(self, model_name: str = "large-v2", device: Optional[str] = None):
        """
        :param model_name: WhisperX model variant (e.g. 'base', 'small', 'medium', 'large-v2')
        :param device: 'cuda' or 'cpu'
        """
        self.model_name = model_name
        self.device = device or ("cuda" if torch.cuda.is_available() else "cpu")
        self.model = None

    def load_model(self):
        import whisperx  # local import (so file doesn’t break if WhisperX isn’t installed yet)
        print(f"[INFO] Loading WhisperX model: {self.model_name} on {self.device}")
        self.model = whisperx.load_model(self.model_name, device=self.device,language="en")
        print("[INFO] WhisperX model loaded successfully.")

    async def transcribe(self, file: str) -> str:
        if self.model is None:
            self.load_model()

        result = self.model.transcribe(file)
        print(result)
        return result
