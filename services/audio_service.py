from models.audio_model import WhisperXTranscriber

transcriber = WhisperXTranscriber(model_name="small")
transcriber.load_model()

async def handle_audio_upload(file):
    transcript = await transcriber.transcribe(file)
    return {"transcription": transcript}
