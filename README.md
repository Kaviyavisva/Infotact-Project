# Prescriptive Maintenance RAG Agent

## Overview
The **Prescriptive Maintenance RAG Agent** is an enterprise-grade AI system designed to analyze maintenance data, diagnose equipment issues, and prescribe actionable maintenance steps using Retrieval-Augmented Generation (RAG) and LangGraph.

## Project Structure
```text
.
├── chroma_db/             # Local vector database storage (ignored by git)
├── logs/                  # Application logs (ignored by git)
├── src/                   # Source code
│   ├── agent/             # LangGraph agent definitions and nodes
│   ├── rag/               # Vector store, retrievers, and document loaders
│   └── utils/             # Helper functions and shared utilities
├── tests/                 # Unit and integration tests
├── .gitignore             # Git ignore file
├── config.py              # Centralized configuration management
├── README.md              # Project documentation
└── requirements.txt       # Python dependencies
```

## Setup Instructions

1. **Create a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Environment Variables:**
   Create a `.env` file in the root directory and add the necessary configuration:
   ```env
   OPENAI_API_KEY=your_openai_api_key_here
   ENVIRONMENT=development
   ```

## Development
- Ensure code follows PEP8 standards.
- Run tests using `pytest tests/`.
