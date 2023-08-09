import speech_recognition as sr
import requests
from io import BytesIO
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/audio_text/<path:audio_url>')

def audio2text(audio_url):
    response = requests.get(audio_url)
    audio_data = BytesIO(response.content)

    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_data) as source:
        audio = recognizer.record(source)

    try:
        text = recognizer.recognize_google(audio)
    except sr.UnknownValueError:
        text = "Speech Recognition could not understand the audio"
    except sr.RequestError as e:
        text = f"Error in accessing the Speech Recognition service: {e}"

    results = {
        'Audio url': audio_url,
        'Audio_text': text
    }

    return jsonify(results)

if __name__ == "__main__":
    app.run(debug=True)
