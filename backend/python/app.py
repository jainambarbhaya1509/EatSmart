from flask import Flask, request, jsonify, send_file
from anythingllm.recipie_generation.recipie_generation import RecipeGeneration
from anythingllm.ingredients.ingredients_awareness import IngredientsAwareness
from anythingllm.health_chatbot.chatbot import Chatbot
from sarvamai import SarvamAI
from sarvamai.play import save
import tempfile
import os


app = Flask(__name__)
client = SarvamAI(api_subscription_key="2da19793-d8bb-4994-a6b7-7badbbfe1f75")

recipeGeneration = RecipeGeneration()
ingredientsAwareness = IngredientsAwareness()
healthChatbot = Chatbot()

# -----------------------------------------------
# ANYTHING LLM API ROUTES ------ NPU OPTIMIZED
# -----------------------------------------------


@app.route("/ingredients-awareness", methods=["POST"])
def ingredients_awareness():
    data = request.get_json()
    message = data.get("message", "")
    response = ingredientsAwareness.chat(message)
    return jsonify({"response": response})

@app.route("/recipe-generation", methods=["POST"])
def recipe_generation():
    data = request.get_json()
    message = data.get("message", "")
    response = recipeGeneration.chat(message)
    return jsonify({"response": response})


@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    message = data.get("message", "")
    response = healthChatbot.chat(message)
    return jsonify({"response": response})



# -----------------------------------------------
# SARVAM AI API ROUTES 
# -----------------------------------------------

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


@app.route('/translate', methods=['POST'])
def translate():
    data = request.get_json()
    print(f"Received data: {data}")
    if not data or 'text' not in data:
        return jsonify({'error': 'Missing text'}), 400

    text = data['text']

    try:
        response = client.text.translate(
            input=text,
            source_language_code="en-IN",
            target_language_code="hi-IN",
            model="sarvam-translate:v1"
        )
        return jsonify({'translated_text': response.translated_text})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)