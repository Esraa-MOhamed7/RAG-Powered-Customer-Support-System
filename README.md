🤖 RAG-Powered Customer Support System
A secure, containerized AI assistant that answers questions strictly from your own data — and refuses to guess.
This project builds a Retrieval-Augmented Generation (RAG) pipeline that reads Amazon policy PDFs and support ticket CSVs, connects to a cloud LLM, and responds with sourced answers. Guardrails block hallucination entirely: if the answer isn't in the data, the system refuses to respond.
✨ Key Features
Multi-format ingestion — PDFs (shipping policies) + CSVs (support tickets)
Anti-hallucination guardrails — strict prompt locking; no answer = no response
Chat interface with dynamic updates (no page reload)
Knowledge Base Console — upload and index files on the fly
Fully containerized — runs on any server instantly via Docker
⚙️ How It Works
Code
Tech Stack
Core AI & Orchestration
Tool
Role
Groq API
Ultra-fast cloud inference
LLaMA-3 / Mixtral
Open-source LLMs for generation
LangChain
RAG pipeline orchestration
PyPDFLoader / CSVLoader
Document ingestion
RecursiveCharacterTextSplitter
Smart text chunking
HuggingFace / OpenAI Embeddings
Text → vectors
ChromaDB / FAISS
Vector database & similarity search
Backend
Tool
Role
Python 3.11
Core language
Flask
API server & routing
Flask Sessions
User state & chat security
python-dotenv
Secrets management
Frontend
Tool
Role
HTML5 / CSS3
Chat UI & Knowledge Base Console
JavaScript (Async/Fetch API)
Dynamic updates without page reload
DevOps
Tool
Role
Docker
Full containerization
Multi-layer Dockerfile
Smart caching — rebuilds in seconds
Port Mapping -p 5000:5000
Container ↔ host traffic
ENV injection
Secure secrets inside the container
🛠️ Development Journey
Stage 1 — Local RAG Pipeline
Built the core pipeline: document ingestion → chunking → embedding → retrieval → generation. Locked the prompt with strict guardrails to prevent hallucination.
Stage 2 — Docker Containerization
Problem: Server not reachable from outside the container.
Fix: Set Flask host to 0.0.0.0 + EXPOSE 5000 + -p 5000:5000 port binding.
Stage 3 — Secrets & Authentication
Problem 1: 401 AuthenticationError — load_dotenv can't read .env files from inside an isolated Docker environment.
Problem 2: Flask session errors from missing SECRET_KEY.
Fix: Injected all environment variables directly via ENV in the Dockerfile — ensuring libraries read them instantly inside the isolated container.
Stage 4 — Final Testing
Problem: System refused to answer after a fresh build — the local vector database wasn't carried into the new container.
Fix: Re-uploaded documents to the clean container.
Results:
✅ Asked about Amazon Germany shipping policy → instant answer citing [Source: Amazon Official Policy]
✅ Asked about a broken mug ticket (file not uploaded) → guardrail fired, system refused to respond
Both scenarios confirmed the system is accurate and fully sealed.
Run Locally
Bash
Open http://localhost:5000 in your browser.
🔒 Security Notes
API keys are never hardcoded — injected via environment variables only
Guardrails prevent the model from generating answers outside the provided context
Docker isolation ensures a clean, reproducible environment
🙏 Note
This project was a deep dive into connecting RAG, LLMs, containerization, and real security practices — built and debugged from scratch through every layer of the stack.
Feedback and suggestions are always welcome!
دا readme fileبتاعه ، بناء عليه عايزين ننزل بوست حلو
