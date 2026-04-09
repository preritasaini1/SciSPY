import os
import requests

# Assuming you have the Gemini API setup with a client
gemini_api_key = os.getenv("AIzaSyAbyZguUXue50Unx0Mgvebj_vmLJMHq358")  # Make sure to set this in your .env file

def transcribe_audio(file_path):
    # Use Gemini API to transcribe audio
    response = requests.post(
        "https://gemini-api.com/transcribe",  # Placeholder URL, replace with actual Gemini endpoint
        headers={"Authorization": f"Bearer {gemini_api_key}"},
        files={"file": open(file_path, "rb")}
    )
    transcription = response.json()  # Assuming the response is in JSON format
    return transcription["text"]

def speak_text(text):
    # Use Gemini API to convert text to speech
    response = requests.post(
        "https://gemini-api.com/speech",  # Placeholder URL, replace with actual Gemini endpoint
        headers={"Authorization": f"Bearer {gemini_api_key}"},
        json={"text": text}
    )
    audio_data = response.content

    # Save audio to file
    audio_dir = "audio"
    os.makedirs(audio_dir, exist_ok=True)
    file_path = os.path.join(audio_dir, "output_audio.mp3")
    with open(file_path, "wb") as f:
        f.write(audio_data)

    return file_path
