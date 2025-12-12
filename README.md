# AI Voice Agent

This project is a scalable AI Voice Agent system with a Python FastAPI backend and a Next.js frontend.

## Prerequisites

- Python 3.10+
- Node.js 18+
- npm

## Getting Started

### Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Create and activate a virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   # On Windows
   venv\Scripts\activate
   # On macOS/Linux
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the server:
   ```bash
   uvicorn app.main:app --reload
   ```
   The API will be available at `http://localhost:8000`.
   API Documentation is available at `http://localhost:8000/docs`.

### Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Run the development server:
   ```bash
   npm run dev
   ```

4. Open [http://localhost:3000](http://localhost:3000) with your browser to see the result.

## Project Structure

- `backend/`: FastAPI application
  - `app/main.py`: Entry point
  - `app/routers/`: API endpoints
  - `app/models.py`: Pydantic models
- `frontend/`: Next.js application
  - `app/`: App router pages
  - `components/`: React components
  - `lib/`: API client utilities
