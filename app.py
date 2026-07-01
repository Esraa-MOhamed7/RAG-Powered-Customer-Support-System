from flask import Flask, render_template, request, session, jsonify,url_for
from langchain_community.document_loaders import PyPDFLoader, CSVLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from dotenv import load_dotenv
from rag import rag_chain, db
import os
import re

app = Flask(__name__)

# 0) SECRETS
load_dotenv("secret.env")
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

#  1) Helper Function: Custom load and split logic

def load_split_data(file, source_type):  
    pdf_pattern = r".*\.pdf$"
    csv_pattern = r".*\.csv$"
    
    # Ensure data directory exists
    os.makedirs("data", exist_ok=True)
    
    # Define file path
    file_path = os.path.join("data", file.filename)
    
    # Save file to disk
    file.save(file_path)
    
    # 1) Load Data
    if re.match(pdf_pattern, file.filename):
        loader = PyPDFLoader(file_path=file_path)
        docs = loader.load()
    elif re.match(csv_pattern, file.filename):
        loader = CSVLoader(file_path=file_path)
        docs = loader.load()
    else:
        return False  
        
    for doc in docs:
        doc.metadata["source"] = source_type
        
    # 2) Split Data
    r_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=100,
        separators=["\n\n", "\n", " ", ""]
    )
    splitts = r_splitter.split_documents(docs)
    
    # 3) Add new documents to database
    db.add_documents(splitts)
    return True

# 2) Flask Routes

# 1) Route one (Return base page)
@app.route("/")
def index():
    session["chat_history"] = []  
    return render_template("index.html")


# 2) Route two (To get user question)
@app.route("/chat", methods=["POST"])
def chat():
    # 1) Get user question from JSON request
    user_question = request.json.get("question")
    if not user_question:
        return jsonify({"Answer": "No question provided"}), 400
        
    # 2) Ensure chat_history exists in session
    if "chat_history" not in session:
        session["chat_history"] = []
        
    # 3) Invoke RAG Chain with current question and history
    response = rag_chain({
        "question": user_question,
        "chat_history": session["chat_history"]
    })
    
    # 4) Append conversation to chat history session
    session["chat_history"].append(("human", user_question))
    session["chat_history"].append(("ai", response))
    session.modified = True  
    
    return jsonify({"answer": response})


#  3) Route three (To get new files)
@app.route("/upload", methods=["POST"])
def upload():
    if 'file-input' not in request.files:
        return jsonify({"error": "No file part in the request"}), 400
        
    file = request.files.get("file-input")
    source_type = request.form.get("source_type")  
    
    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400
        
    success = load_split_data(file=file, source_type=source_type)
    
    if success:
        return jsonify({"message": f"File '{file.filename}' uploaded and indexed successfully into '{source_type}'!"})
    else:
        return jsonify({"error": "Unsupported file format"}), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)