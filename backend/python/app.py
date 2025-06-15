from flask import Flask, request, jsonify, send_file
from anythingllm.recipie_generation import RecipeGeneration
from anythingllm.ingredients_awareness import IngredientsAwareness
from anythingllm.chatbot import Chatbot
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



# -----------------------------------------------
# RAG AI API ROUTES 
# -----------------------------------------------


from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import Chroma
from langchain_ollama import OllamaEmbeddings, ChatOllama
import tempfile
import os


ollama_endpoint = "http://127.0.0.1:11434"
ollama_model = "llama3.2"
ollama = ChatOllama(model=ollama_model, base_url=ollama_endpoint)

vectorstore = None
retriever = None
chat_history = []

def load_and_embed(pdf_file):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
        tmp_file.write(pdf_file.read())
        tmp_pdf_path = tmp_file.name

    loader = PyPDFLoader(tmp_pdf_path)
    docs = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=200, chunk_overlap=40)  # Finer chunks, more overlap
    splits = text_splitter.split_documents(docs)
    embeddings = OllamaEmbeddings(model=ollama_model, base_url=ollama_endpoint)
    vectorstore = Chroma.from_documents(documents=splits, embedding=embeddings)
    os.remove(tmp_pdf_path)
    return vectorstore

def ollama_llm(question, context, chat_history):
    history = "\n".join([f"User: {q}\nAI: {a}" for q, a in chat_history[-5:]])  # Use last 5 exchanges for more context
    prompt = (
        f"{history}\nUser: {question}\n\n"
        f"Context:\n{context}\n"
        "AI: Please answer using only the provided context. Be precise, concise, and limit your response to 1-2 sentences."
    )
    response = ollama.invoke([('human', prompt)])
    return response.content.strip()

def combine_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs[:5])  # Use top 5 docs for richer context

def rag_chain(question):
    retrieved_docs = retriever.invoke(question)
    formatted_context = combine_docs(retrieved_docs)
    answer = ollama_llm(question, formatted_context, chat_history)
    return answer, formatted_context

@app.route('/upload_pdf', methods=['POST'])
def upload_pdf():
    global vectorstore, retriever, chat_history
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    vectorstore = load_and_embed(file)
    retriever = vectorstore.as_retriever()
    chat_history = []
    return jsonify({"message": "PDF processed and vectorstore created."})

@app.route('/ask', methods=['POST'])
def ask():
    global chat_history
    data = request.get_json()
    question = data.get('question')
    if not question:
        return jsonify({"error": "No question provided"}), 400
    if retriever is None:
        return jsonify({"error": "No PDF uploaded yet."}), 400
    answer, context = rag_chain(question)
    chat_history.append((question, answer))
    return jsonify({
        "answer": answer,
        "context": context,
        "chat_history": chat_history
    })


if __name__ == "__main__":
    app.run(debug=True)