from flask import Flask, request, send_file, jsonify
from sarvamai import SarvamAI
from sarvamai.play import save
import tempfile
import os

app = Flask(__name__)

client = SarvamAI(api_subscription_key="2da19793-d8bb-4994-a6b7-7badbbfe1f75")

@app.route('/tts', methods=['POST'])
def tts():
    data = request.get_json()
    if not data or 'text' not in data:
        return jsonify({'error': 'Missing text'}), 400

    text = data['text']
    audio = client.text_to_speech.convert(
        target_language_code="en-IN",
        text=text,
        model="bulbul:v2",
        speaker="anushka"
    )

    with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as tmp_file:
        tmp_path = tmp_file.name
    save(audio, tmp_path)
    print(f"Audio saved to file: {tmp_path}")

    response = send_file(tmp_path, mimetype='audio/wav', as_attachment=True, download_name='output.wav')
    # Clean up the temp file after sending
    @response.call_on_close
    def cleanup():
        os.remove(tmp_path)
    return response


@app.route('/stt', methods=['POST'])
def stt():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    # Save the uploaded file to a temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as tmp_file:
        file.save(tmp_file)
        tmp_path = tmp_file.name

    try:
        with open(tmp_path, "rb") as audio_file:
            response = client.speech_to_text.transcribe(
                file=audio_file,
                model="saarika:v2",
            )
        return jsonify({'text': response.transcript})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)

if __name__ == '__main__':
    app.run(debug=True)
