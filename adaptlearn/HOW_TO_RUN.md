# 🏃 How to Run AdaptLearn AI

Follow these steps to get the full system running locally.

## Prerequisities
*   Node.js (v18+)
*   Python (v3.10+)

## 1. Backend Setup

Open a terminal in the `adaptlearn/backend` folder:

```bash
cd backend
# Create virtual environment
python -m venv venv

# Activate it
# Windows:
.\venv\Scripts\activate
# Mac/Linux: source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Start the server
uvicorn main:app --reload
```

The Backend is now running at `http://localhost:8000`.

## 2. Frontend Setup

Open a **new** terminal in the `adaptlearn/frontend` folder:

```bash
cd frontend

# Install dependencies
npm install

# Start the development server
npm run dev
```

The Frontend is now running at `http://localhost:3000`.

## 3. Environment Variables (IMPORTANT)

You **MUST** create `.env` files for the app to work. These are ignored by git for security.

**Backend (`backend/.env`):**
```ini
DATABASE_URL=sqlite:///./sql_app.db
SECRET_KEY=your_super_secret_key_here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_CLIENT_SECRET=your_google_client_secret
GEMINI_API_KEY=your_gemini_api_key
```

**Frontend (`frontend/.env.local`):**
```ini
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_GOOGLE_CLIENT_ID=your_google_client_id
```

## 4. Usage

1.  Go to `http://localhost:3000`.
2.  Sign up with Email or Google.
3.  Start chatting with the AI.
4.  Ask to "Test my knowledge" to see the adaptive quiz system in action.
