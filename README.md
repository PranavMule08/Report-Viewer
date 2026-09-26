```markdown

\# Report Viewer



📄 \*\*Report Viewer\*\* is a full-stack, AI-powered web application designed to upload, analyze, and review document reports with an interactive AI chat interface.



\---



\## 🌟 Features



\- \*\*Document Analysis\*\*: Upload report files (TXT, PDF, etc.) and generate automated AI summaries and structured reviews.

\- \*\*Interactive AI Chat\*\*: Ask questions and chat directly with your uploaded documents in real time.

\- \*\*User Authentication\*\*: Complete user registration and login system with secure JWT session handling.

\- \*\*Dashboard \& History\*\*: Track, view, and manage all your past uploaded reports and AI-generated reviews in one place.

\- \*\*Dark/Light Theme\*\*: Sleek, modern UI with support for customized themes.



\---



\## 🛠️ Tech Stack



\- \*\*Frontend\*\*: React (Vite), JavaScript, CSS3, React Router

\- \*\*Backend\*\*: Python 3.13, FastAPI, SQLite / SQLAlchemy

\- \*\*AI Integration\*\*: Custom AI Service for document processing and conversational QA



\---



\## 🚀 Quick Start



\### Local Development



\#### 1. Backend Setup



```bash

cd report\_reviewer/backend



\# Create virtual environment

python -m venv venv



\# Activate virtual environment

\# On Windows:

venv\\Scripts\\activate

\# On Mac/Linux:

source venv/bin/activate



\# Install dependencies

pip install -r requirements.txt



\# Start backend server

uvicorn app.main:app --reload



```



\* \*\*Backend runs at\*\*: `http://localhost:8000`

\* \*\*API Docs\*\*: `http://localhost:8000/docs`



\---



\#### 2. Frontend Setup



Open a new terminal tab or window:



```bash

cd report\_reviewer/frontend



\# Install dependencies

npm install



\# Start development server

npm run dev



```



\* \*\*Frontend runs at\*\*: `http://localhost:5173`



\---



\## 📦 Deployment Options



\### Option 1: Deploy to Render (Recommended - Free)



1\. Push your repository to GitHub.

2\. Go to \[https://render.com](https://render.com?utm\_source=gemini) and create an account.

3\. \*\*Deploy Backend\*\*:

\* Click \*\*New +\*\* → \*\*Web Service\*\*

\* Connect your GitHub repository

\* \*\*Root Directory\*\*: `report\_reviewer/backend`

\* \*\*Build Command\*\*: `pip install -r requirements.txt`

\* \*\*Start Command\*\*: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`





4\. \*\*Deploy Frontend\*\*:

\* Click \*\*New +\*\* → \*\*Static Site\*\*

\* \*\*Root Directory\*\*: `report\_reviewer/frontend`

\* \*\*Build Command\*\*: `npm run build`

\* \*\*Publish Directory\*\*: `dist`







\---



\## 🔧 API Endpoints



\### Health \& Auth



\* `POST /api/auth/register` — Register a new user

\* `POST /api/auth/login` — Authenticate user and issue token



\### Reports \& Review



\* `POST /api/upload` — Upload a new report document

\* `GET /api/reports` — Fetch all uploaded reports

\* `GET /api/reviews/{report\_id}` — Get AI review for a specific report

\* `POST /api/chat` — Send query to AI regarding uploaded documents



\---



\## 🔒 Security Features



\* Secure password hashing

\* CORS protection configured between frontend and backend

\* Untracked `.env` configuration for sensitive keys and DB connections

\* File-upload sanitization



\---



\## 📊 Project Structure



```text

Report\_Viewer/

└── report\_reviewer/

&#x20;   ├── backend/

&#x20;   │   ├── app/

&#x20;   │   │   ├── api/          # Route handlers (auth, reports, chat, upload)

&#x20;   │   │   ├── core/         # Config \& security settings

&#x20;   │   │   ├── db/           # Database sessions \& models

&#x20;   │   │   ├── models/       # Database schemas

&#x20;   │   │   └── services/     # AI service \& file extraction logic

&#x20;   │   ├── main.py           # FastAPI entrypoint

&#x20;   │   └── requirements.txt  # Python packages

&#x20;   └── frontend/

&#x20;       ├── src/

&#x20;       │   ├── context/      # AuthContext state management

&#x20;       │   ├── pages/        # Dashboard, Chat, ReportReview, Upload

&#x20;       │   └── services/     # API Axios client

&#x20;       ├── index.html        # Entry HTML

&#x20;       └── vite.config.js    # Vite configuration



```



\---



\## 🤝 Contributing



Contributions, issues, and feature requests are welcome!



\---



\## 📝 License



MIT License - Use freely for personal and educational projects.



\---



\## 📧 Support



For issues or questions, feel free to open an issue in the repository.



Made with ❤️ by \*\*Pranav Mule\*\* | Report Viewer v1.0.0



```



```

