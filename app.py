import logging
import os
import speech_recognition as sr
import requests
from io import BytesIO
from flask import Flask, jsonify
logging.basicConfig(filename='app.log', level=logging.DEBUG)
#g
app = Flask(__name__)
@app.route('/<path:audio_url>')
#/audio_text
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
        'Audio_url': audio_url,
        'Audio_text': text
    }
    #----------------- Send the results JSON to the desired API
    api_url = "https://lms.cgit.pk/api.php?action=text_to_speech"
    
    headers = {
        'Content-Type': 'application/json',
        'Cookie': 'PHPSESSID=ceaed9ceeee61626319a5dc145f36877'
    }
    api_response = requests.request("POST",url=api_url, headers=headers, json=results)

    if api_response.status_code == 200:
        #It will print the response for POSTING on terminal
        print(api_response.text)
    else:
        return jsonify({"error": "Failed to send data to API"})
    
    #It will print GET response on Local Host
    return jsonify(results)

if __name__ == "__main__":
    port = int(os.getenv('PORT', 5000))  # Use default value 5000 if PORT is not set
    app.run(host="0.0.0.0", port=port)

