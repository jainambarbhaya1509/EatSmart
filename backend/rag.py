from flask import Flask, request, jsonify
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import Chroma
from langchain_ollama import OllamaEmbeddings, ChatOllama
import tempfile
import os

app = Flask(__name__)

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
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=10)
    splits = text_splitter.split_documents(docs)
    embeddings = OllamaEmbeddings(model=ollama_model, base_url=ollama_endpoint)
    vectorstore = Chroma.from_documents(documents=splits, embedding=embeddings)
    os.remove(tmp_pdf_path)
    return vectorstore

def ollama_llm(question, context, chat_history):
    history = "\n".join([f"User: {q}\nAI: {a}" for q, a in chat_history])
    prompt = f"{history}\nUser: {question}\n\nContext: {context}\nAI:"
    response = ollama.invoke([('human', prompt)])
    return response.content.strip()

def combine_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

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

if __name__ == '__main__':
    app.run(debug=True)
