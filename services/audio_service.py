from models.audio_model import WhisperXTranscriber
from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline

transcriber = WhisperXTranscriber(model_name="large-v2")
transcriber.load_model()
save_directory = "models/distilbert-base-uncased-hate-speech-checker/best-weight"


async def handle_audio_upload(file):
    print("Recieved upload")
    transcript_result = await transcriber.transcribe(file)
    print(transcript_result)
    model = AutoModelForSequenceClassification.from_pretrained(save_directory)

    # Load the tokenizer
    tokenizer = AutoTokenizer.from_pretrained(save_directory)
    inferencer = pipeline("text-classification", model=model, tokenizer=tokenizer)
    for res in transcript_result["segments"]:
        results = inferencer(res['text'])

        print(results)
        res['label']=results[0]['label']
        res['score'] = results[0]['score']
    
    return transcript_result
