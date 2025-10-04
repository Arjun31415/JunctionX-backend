import os
import tempfile
from pydub import AudioSegment
from models.audio_model import WhisperXTranscriber
from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline

transcriber = WhisperXTranscriber(model_name="large-v2")
transcriber.load_model()
save_directory = "models/distilbert-base-uncased-hate-speech-checker/best-weight"

async def handle_audio_upload(file):
    # Save uploaded file temporarily
    suffix = os.path.splitext(file.filename)[-1].lower()
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as temp_input:
        contents = await file.read()
        temp_input.write(contents)
        temp_input_path = temp_input.name

    # Convert MP4 -> MP3 if needed
    if suffix == ".mp4":
        temp_output_path = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3").name
        audio = AudioSegment.from_file(temp_input_path, format="mp4")
        audio.export(temp_output_path, format="mp3")
        os.remove(temp_input_path)  # remove original MP4
        audio_path = temp_output_path
    else:
        audio_path = temp_input_path

    # Transcribe the (possibly converted) audio file
    transcript_result = await transcriber.transcribe(audio_path)
    print(transcript_result)

    # Load the classification model
    model = AutoModelForSequenceClassification.from_pretrained(save_directory)
    tokenizer = AutoTokenizer.from_pretrained(save_directory)
    inferencer = pipeline("text-classification", model=model, tokenizer=tokenizer)

    # Run classification for each segment
    for res in transcript_result["segments"]:
        results = inferencer(res["text"])
        res["label"] = results[0]["label"]
        res["score"] = results[0]["score"]

    # Clean up temporary files
    os.remove(audio_path)

    return transcript_result
