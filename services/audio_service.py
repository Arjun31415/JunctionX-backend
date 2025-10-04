from models.audio_model import WhisperXTranscriber

transcriber = WhisperXTranscriber(model_name="large-v2")
transcriber.load_model()

async def handle_audio_upload(file):
    transcript_result = await transcriber.transcribe(file)
    return transcript_result
