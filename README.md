# 🤖 RAG-Powered Customer Support System

A secure, containerized AI assistant that answers questions strictly from your own data — and refuses to guess.

This project implements a Retrieval-Augmented Generation (RAG) pipeline capable of reading multiple document formats, retrieving relevant information, and generating grounded responses using Large Language Models (LLMs).

The system supports Amazon policy PDFs and customer support ticket CSVs while preventing hallucinations through strict guardrails.

---

## Project Overview

The goal of this project was to build a customer support assistant that:

* Reads documents dynamically
* Retrieves only relevant context
* Generates sourced responses
* Rejects unsupported questions
* Runs consistently inside an isolated Docker environment

Unlike traditional chatbots, this system is designed to answer only from uploaded knowledge.

---

## ✨ Features

* Multi-format ingestion (PDF + CSV)
* Retrieval-Augmented Generation (RAG)
* Context-aware answer generation
* Anti-hallucination guardrails
* Interactive chat interface
* Dynamic document upload & indexing
* Dockerized deployment
* Secure environment configuration

---

## 🏗️ System Architecture

User Query
↓
Document Retrieval
↓
Chunk Selection
↓
Embedding Search
↓
LLM Generation
↓
Guardrails Validation
↓
Final Response + Source

---

## 🧠 Tech Stack

### Core AI & Orchestration

| Tool                            | Purpose             |
| ------------------------------- | ------------------- |
| Groq API                        | Cloud inference     |
| LLaMA-3 / Mixtral               | Response generation |
| LangChain                       | RAG orchestration   |
| PyPDFLoader                     | PDF ingestion       |
| CSVLoader                       | CSV ingestion       |
| RecursiveCharacterTextSplitter  | Chunking            |
| HuggingFace / OpenAI Embeddings | Vector generation   |
| ChromaDB / FAISS                | Vector database     |

---

### Backend

| Tool           | Purpose               |
| -------------- | --------------------- |
| Python 3.11    | Core language         |
| Flask          | API & routing         |
| Flask Sessions | Session handling      |
| python-dotenv  | Environment variables |

---

### Frontend

| Tool         | Purpose         |
| ------------ | --------------- |
| HTML5 / CSS3 | UI              |
| JavaScript   | Dynamic updates |

---

### DevOps

| Tool         | Purpose              |
| ------------ | -------------------- |
| Docker       | Containerization     |
| Dockerfile   | Environment setup    |
| Port Mapping | Container networking |

---

## Guardrails

The system follows strict grounding rules:

* Responses must come only from retrieved context
* Unsupported questions are rejected
* No generation outside uploaded documents
* Source attribution is enforced

---

## Getting Started

### Clone Repository

```bash
git clone <repo-url>
cd <project-folder>
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Configure Environment

Create `.env`

```env
GROQ_API_KEY=your_key
SECRET_KEY=your_secret
```

### Run Locally

```bash
python app.py
```

Open:

```text
http://localhost:5000
```

---

## 🐳 Run with Docker

### Build

```bash
docker build -t rag-support .
```

### Run

```bash
docker run -p 5000:5000 --env-file .env rag-support
```

---

## 🧪 Example Scenarios

### Valid Question

Question:

```text
What is Amazon's shipping policy for Germany?
```

Result:

```text
Answer returned with source citation.
```

### Unsupported Question

Question:

```text
What is Amazon's refund policy in Japan?
```

Result:

```text
I cannot answer because this information does not exist in the uploaded documents.
```

---

## Future Improvements

* User authentication
* Streaming responses
* Conversation memory
* Production deployment
* Multi-user support

---

## 🙏 Acknowledgment

This project was built to explore RAG systems, LLM integration, Docker deployment, and building safer AI applications.
