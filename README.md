# AdaptLearn AI 🧠

AdaptLearn AI is a next-generation adaptive learning platform that personalizes education using advanced Artificial Intelligence. Unlike traditional functional LMS platforms, AdaptLearn actively analyzes your interactions, adjusts curriculum difficulty in real-time, and provides instant, context-aware tutoring.

## 🚀 Tech Stack

### Frontend
*   **Framework**: Next.js 15+ (App Router, Turbopack)
*   **Language**: TypeScript
*   **Styling**: Tailwind CSS v4, Framer Motion (Animations), Lucide React (Icons)
*   **State/Data**: React Hooks, Axios
*   **Visuals**: Custom 3D Neural visualizations, Glassmorphism UI

### Backend
*   **Framework**: FastAPI (Python)
*   **Database**: SQLite (Dev) / PostgreSQL (Prod ready), SQLAlchemy ORM
*   **Authentication**: OAuth2 (Google & Email/Password), JWT (Argon2/PBKDF2 hashing)
*   **AI Engine**: Google Gemini Pro & Ollama (Llama 3) integration for context-aware generation.

## 🏗️ Architecture & Implementation

We built AdaptLearn with a clean **Service-Oriented Architecture**:

1.  **AI Service Layer**: A dedicated `LLMService` handles prompts to Gemini/Ollama. It includes fallback logic and structured JSON parsing to ensure the AI returns usable data for quizzes and summaries, not just raw text.
2.  **Adaptive Logic**:
    *   **Quiz Generation**: The system reads your specific chat context and dynamically constructs 4-option multiple choice questions to test exactly what you just discussed.
    *   **Progress Tracking**: Every interaction is logged as a `LearningEvent`. The backend aggregates these events to visualize your "Cognitive Momentum" over time.
3.  **Modern Security**: Robust auth implementation using `OAuth2PasswordBearer`, secure hashing (PBKDF2), and HTTP-only standards. All sensitive keys are strictly environment-scoped.
4.  **Frontend-Backend Sync**: The Next.js frontend is tightly coupled to the FastAPI schema via a custom API client (`api.ts`) that handles token interception, automatic refreshing, and error normalization.

## ✨ Key Features

*   **Neural Adaptation**: The system learns from you. If you ask advanced questions, the AI shifts its tone and content depth automatically.
*   **Interactive Neural Core**: A bespoke 3D-animated hero section that visualizes the "living" nature of the platform.
*   **Context-Resonant Quizzes**: No pre-canned questions. Quizzes are generated on the fly based on your unique conversation history.
*   **Dark Mode Native**: Built from the ground up for a premium, high-contrast dark aesthetic with neon accents.
