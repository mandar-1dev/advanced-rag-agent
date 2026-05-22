# Advanced RAG Agent

A starter scaffold for an advanced Retrieval-Augmented Generation (RAG) agent.

## Structure

- `backend/` — FastAPI backend and RAG pipeline
- `frontend/` — Vite + React frontend

## Usage

1. Install backend dependencies:
   ```bash
   python -m pip install -r backend/requirements.txt
   ```
2. Start the backend:
   ```bash
   uvicorn backend.main:app --reload --port 8000
   ```
3. Install frontend dependencies:
   ```bash
   cd frontend
   npm install
   npm run dev
   ```
