from flask import Flask, render_template, request
import speech_recognition as sr
import os

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    audio_file = request.files['audio']

    if audio_file.filename == '':
        return "No file selected"

    filepath = os.path.join(UPLOAD_FOLDER, audio_file.filename)
    audio_file.save(filepath)

    recognizer = sr.Recognizer()

    try:
        with sr.AudioFile(filepath) as source:
            audio_data = recognizer.record(source)

        text = recognizer.recognize_google(audio_data)

        return f"""
        <h2>Converted Text</h2>
        <p>{text}</p>
        <br>
        <a href="/">Go Back</a>
        """

    except Exception as e:
        print("FULL ERROR:", repr(e))
        return f"<h3>Error</h3><p>{repr(e)}</p>"

if __name__ == '__main__':
    app.run(debug=True)