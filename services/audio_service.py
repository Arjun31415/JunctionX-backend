from models.audio_model import DummyAudioTranscriber

transcriber = DummyAudioTranscriber()
transcriber.load_model()

async def handle_audio_upload(file):
    transcript = await transcriber.transcribe(file)
    return {"transcription": transcript}
