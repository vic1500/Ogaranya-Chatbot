# 🤖 Ogaranya AI Support Bot

A full-stack Retrieval-Augmented Generation (RAG) chatbot designed to provide instant, highly accurate customer and merchant support for the **Ogaranya** Offline-to-Online (O2O) commerce platform. 

This project uses a "Hybrid AI" approach: it embeds and searches the company's knowledge base locally using an open-source HuggingFace model, and uses Groq's `llama-3.1-8b-instant` model to formulate conversational, context-aware responses.

## ✨ Features
* **Custom Knowledge Base:** Answers are restricted *strictly* to the provided Ogaranya documentation to prevent AI hallucinations.
* **Hybrid RAG Architecture:** 
  * **Memory:** Local ChromaDB vector database using a lightweight HuggingFace embedding model (`all-MiniLM-L6-v2`).
  * **Brain:** Cloud-based LLM generation using the Groq API.
* **Lightning Fast Backend:** Built with FastAPI and LangChain for asynchronous, non-blocking API requests.
* **Sleek Frontend UI:** A modern, responsive React + Vite frontend featuring Dark Mode, Glassmorphism elements, Tailwind CSS styling, and custom scrollbars.

---

## 🛠️ Tech Stack

**Backend (Python)**
* [FastAPI](https://fastapi.tiangolo.com/) - High-performance web framework
* [LangChain](https://python.langchain.com/) - LLM orchestration framework
* [ChromaDB](https://www.trychroma.com/) - Local vector database
* [HuggingFace Embeddings](https://huggingface.co/) - Document vectorization
* [Groq](https://cohere.com/) - Large Language Model (`llama-3.1-8b-instant`)
* [uv](https://github.com/astral-sh/uv) - Extremely fast Python package installer and resolver

**Frontend (JavaScript)**
* [React](https://react.dev/) - UI Library
* [Vite](https://vitejs.dev/) - Frontend tooling and bundler
* [Tailwind CSS](https://tailwindcss.com/) - Utility-first CSS framework

---

## 🚀 Getting Started

### Prerequisites
Before you begin, ensure you have the following installed on your machine:
* **Python 3.9+**
* **Node.js** (v16 or higher)
* **uv** (`pip install uv`)
* A free [Groq API Key](https://dashboard.cohere.com/)

### 1. Backend Setup

1. **Install Python dependencies using `uv`:**
   ```bash
   uv pip install -r requirements.txt
   ```
   
2. **Add your Knowledge Base:**
   Ensure your `formatted_knowledge_base.txt` file is in the data directory of the backend directory. If you don't have one then you can run the scraper by running
    ```bash
   uv run python app/utils/scraper.py
   ```
   Then take the generated `ogaranya_knowledge_base.txt` file and use an AI model (gemini, chatgpt, groq) to extract relevant and essential information and organize the text. Then take the organized text and put it in `formatted_knowledge_base.txt` in the data directory of the backend directory.

3. **Build the Vector Database:**
   Run the ingestion script to chunk your text file and save it to the local `chroma_db` folder.
   ```bash
   uv run python app/utils/ingest.py
   ```

4. **Set up your API Key and Run the Server**
    Create a `.env` file in the backend directory and paste your `GROQ_API_KEY`. Then start the FastApi server:
    ```bash
   uv run uvicorn main:app
   ```
    _The backend will be running at `http://localhost:8000`_

### 2. Frontend Setup
1. **Navigate to the frontend directory**
    ```bash
    cd frontend
    ```
   
2. **Install Node dependencies**
    ```bash
   npm install
   ```
   
3. **Start the Vite development server**
    ```bash
   npm run dev
   ```
   _The frontend will now be running at `http://localhost:5173`_

---
## 🧪 Example Test Questions
Once the app is running, try asking the bot these questions to see the RAG pipeline in action:

* "What is OgaPay and how do I use it to send an invoice?"

* "How do I buy 1000 Naira airtime for my MTN number?"

* "What is the difference between a virtual account and a wallet?"

* "How do I book a flight to London?" (The bot should politely decline, as this is outside its knowledge base).