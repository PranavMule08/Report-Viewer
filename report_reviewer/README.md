# AI-Powered Project Report Reviewer and Improvement Assistant Using Generative AI

## Final Year College Project

A complete web application that allows students to upload their academic/project reports and use Generative AI to automatically review the report, identify problems, provide suggestions, and help improve the report.

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.9+-blue.svg)
![FastAPI](https://img.shields.io/badge/fastapi-0.104+-green.svg)
![React](https://img.shields.io/badge/react-18+-blue.svg)

---

## Features

### Core Features

1. **User Authentication**
   - Sign Up / Registration
   - Login / Logout
   - JWT-based session management
   - Secure password hashing with bcrypt

2. **Dashboard**
   - Total reports reviewed
   - Reports currently being processed
   - Average report score
   - Recent reports list
   - Quick upload button

3. **Report Upload**
   - Supported formats: PDF, DOCX, TXT
   - File type validation
   - File size validation (10MB max)
   - Upload status tracking

4. **Text Extraction**
   - PDF: Page-by-page text extraction using pdfplumber
   - DOCX: Paragraph and table extraction using python-docx
   - TXT: Direct text reading with encoding detection

5. **Generative AI Integration**
   - Real OpenAI API integration (GPT-4/GPT-3.5)
   - Secure API key storage in environment variables
   - Chunking for large documents
   - Structured JSON responses
   - Error handling and rate limiting

6. **AI Review System**
   - Overall score (0-100)
   - Category scores (Grammar, Content, Structure, Clarity, Academic Style)
   - Overall quality level
   - Summary assessment
   - Strengths identification
   - Weaknesses identification
   - Priority recommendations

7. **Section-wise Analysis**
   - Automatic section detection
   - Per-section scoring
   - Section strengths and weaknesses
   - Improvement suggestions
   - Priority levels

8. **Issue Detection**
   - Categorized issues (Grammar, Spelling, Content, Structure, etc.)
   - Severity levels (Critical, High, Medium, Low)
   - Location references
   - Suggested corrections

9. **AI Improvement Assistant**
   - Text improvement types: rewrite, academic, concise, expand, grammar, technical, simplify
   - Side-by-side comparison (original vs improved)
   - Copy to clipboard functionality

10. **AI Chat Assistant**
    - Report-specific context-aware chat
    - Suggested questions
    - Interactive conversation

11. **Review History**
    - Previous reports list
    - Review dates and scores
    - View full review
    - Delete reports

---

## Technology Stack

### Backend
- **Framework**: Python FastAPI
- **Database**: SQLite with SQLAlchemy (async)
- **Authentication**: JWT with python-jose
- **Password Hashing**: bcrypt via passlib
- **File Processing**: pdfplumber, python-docx
- **AI Integration**: OpenAI API (or compatible)
- **HTTP Client**: httpx (async)

### Frontend
- **Framework**: React 18
- **Build Tool**: Vite
- **Routing**: React Router DOM
- **HTTP Client**: Axios
- **Icons**: Lucide React
- **Charts**: Recharts (optional)

### Architecture
```
report_reviewer/
├── backend/
│   ├── app/
│   │   ├── api/           # API endpoints
│   │   ├── core/          # Configuration, security, dependencies
│   │   ├── db/            # Database session and models base
│   │   ├── models/        # SQLAlchemy models
│   │   ├── schemas/       # Pydantic schemas
│   │   ├── services/      # Business logic (AI, file extraction)
│   │   └── main.py        # FastAPI application entry
│   ├── uploads/           # Uploaded files storage
│   ├── requirements.txt   # Python dependencies
│   └── .env               # Environment variables
├── frontend/
│   ├── src/
│   │   ├── components/    # React components
│   │   ├── pages/         # Page components
│   │   ├── services/      # API service
│   │   ├── context/       # React context providers
│   │   ├── hooks/         # Custom hooks
│   │   ├── App.jsx        # Main app component
│   │   └── main.jsx       # Entry point
│   ├── .env               # Frontend environment
│   └── package.json       # Node dependencies
├── .env.example           # Example environment variables
└── README.md              # This file
```

---

## Requirements

### System Requirements
- Python 3.9 or higher
- Node.js 16 or higher
- npm or yarn

### Python Dependencies
See `backend/requirements.txt`:
- fastapi
- uvicorn
- sqlalchemy
- aiosqlite
- python-jose
- passlib[bcrypt]
- python-docx
- PyPDF2
- pdfplumber
- python-dotenv
- httpx
- aiofiles
- email-validator

### Node Dependencies
See `frontend/package.json`:
- react
- react-router-dom
- axios
- lucide-react

---

## Installation

### 1. Clone or Extract the Project

```bash
cd report_reviewer
```

### 2. Backend Setup

```bash
cd backend

# Create virtual environment (recommended)
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file (copy from .env.example)
copy .env.example .env    # Windows
cp .env.example .env      # macOS/Linux
```

### 3. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Create .env file (copy from .env.example)
copy .env.example .env    # Windows
cp .env.example .env      # macOS/Linux
```

---

## Environment Variables

### Backend (.env)

| Variable | Description | Default |
|----------|-------------|---------|
| `SECRET_KEY` | JWT secret key (change in production) | `your-secret-key...` |
| `OPENAI_API_KEY` | OpenAI API key (get from platform.openai.com) | (not set) |
| `OPENAI_MODEL` | OpenAI model to use | `gpt-4` |
| `DEMO_MODE` | Run without API key (simulated responses) | `true` (for demo) |
| `MAX_FILE_SIZE_MB` | Maximum file size in MB | `10` |
| `CORS_ORIGINS` | Allowed frontend origins | `http://localhost:5173` |

### Frontend (.env)

| Variable | Description | Default |
|----------|-------------|---------|
| `VITE_API_URL` | Backend API URL | `http://localhost:8000/api/v1` |

---

## Running the Application

### Start Backend

```bash
cd backend

# Activate virtual environment if not already active
# venv\Scripts\activate (Windows)
# source venv/bin/activate (macOS/Linux)

# Run the server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The backend will be available at `http://localhost:8000`

API documentation: `http://localhost:8000/docs`

### Start Frontend

```bash
cd frontend

# Run development server
npm run dev
```

The frontend will be available at `http://localhost:5173`

---

## Usage

### 1. Access the Application
Open your browser and navigate to `http://localhost:5173`

### 2. Create an Account
Click "Get Started" or navigate to `/register`

### 3. Login
Use your credentials to log in

### 4. Upload a Report
- Click "Upload Report" in the sidebar
- Drag and drop or click to select a file
- Supported formats: PDF, DOCX, TXT
- Maximum file size: 10MB

### 5. View Analysis
- Go to "My Reports" to see your uploaded files
- Click "View Review" on a completed report
- Explore the analysis tabs: Overview, Sections, Issues, AI Chat

### 6. Use AI Improvement
- In the report review, select a section
- Use the AI Improvement Assistant to rewrite or improve text
- Compare original and improved versions

### 7. Chat with AI
- Use the AI Chat tab to ask questions about your report
- Get suggestions and guidance from the AI assistant

---

## Demo Mode

When `DEMO_MODE=true` or `OPENAI_API_KEY` is not set, the application runs in demo mode:

- Simulated AI analysis based on text heuristics
- Realistic-looking but not actual AI responses
- Clearly marked as "Demo Mode" in the UI
- Useful for development and testing without API costs

To use real AI:

1. Get an API key from [OpenAI](https://platform.openai.com/api-keys)
2. Set `OPENAI_API_KEY=sk-...` in backend/.env
3. Set `DEMO_MODE=false` in backend/.env
4. Restart the backend server

---

## API Endpoints

### Authentication
- `POST /api/v1/auth/register` - Register new user
- `POST /api/v1/auth/login/json` - Login (JSON body)
- `GET /api/v1/auth/me` - Get current user
- `POST /api/v1/auth/logout` - Logout

### Reports
- `GET /api/v1/reports` - List user's reports
- `GET /api/v1/reports/dashboard` - Dashboard statistics
- `GET /api/v1/reports/{id}` - Get report details
- `GET /api/v1/reports/{id}/review` - Get report review
- `DELETE /api/v1/reports/{id}` - Delete report

### Upload
- `POST /api/v1/upload/upload` - Upload a file
- `GET /api/v1/upload/status/{id}` - Check upload status

### Reviews
- `POST /api/v1/reviews/{report_id}/analyze` - Trigger AI analysis
- `GET /api/v1/reviews/{report_id}/review-data` - Get full review data
- `POST /api/v1/reviews/improve` - Improve text with AI

### Chat
- `POST /api/v1/chat` - Chat about a report
- `GET /api/v1/chat/suggested-questions?report_id={id}` - Get suggested questions
- `GET /api/v1/chat/context/{report_id}` - Get report context

---

## Database Schema

### Users Table
| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER | Primary key |
| name | VARCHAR(100) | User's full name |
| email | VARCHAR(255) | User's email (unique) |
| password_hash | VARCHAR(255) | Bcrypt hashed password |
| created_at | DATETIME | Account creation timestamp |

### Reports Table
| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER | Primary key |
| user_id | INTEGER | Foreign key to users |
| filename | VARCHAR(255) | Stored filename |
| original_filename | VARCHAR(255) | Original file name |
| file_path | VARCHAR(500) | Path to stored file |
| file_size | INTEGER | File size in bytes |
| file_type | VARCHAR(20) | File extension |
| extracted_text | TEXT | Extracted content |
| upload_date | DATETIME | Upload timestamp |
| status | VARCHAR(20) | Processing status |
| error_message | TEXT | Error details if failed |

### Reviews Table
| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER | Primary key |
| report_id | INTEGER | Foreign key to reports |
| overall_score | FLOAT | Overall score (0-100) |
| overall_quality | VARCHAR(50) | Quality level |
| summary | TEXT | Review summary |
| strengths | JSON | List of strengths |
| weaknesses | JSON | List of weaknesses |
| recommendations | JSON | List of recommendations |
| grammar_score | FLOAT | Grammar score |
| content_score | FLOAT | Content score |
| structure_score | FLOAT | Structure score |
| clarity_score | FLOAT | Clarity score |
| academic_style_score | FLOAT | Academic style score |
| created_at | DATETIME | Review timestamp |

### Section Reviews Table
| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER | Primary key |
| review_id | INTEGER | Foreign key to reviews |
| section_name | VARCHAR(255) | Section name |
| section_order | INTEGER | Section order |
| score | FLOAT | Section score |
| content_preview | TEXT | Text preview |
| strengths | JSON | Section strengths |
| weaknesses | JSON | Section weaknesses |
| suggestions | JSON | Improvement suggestions |
| priority | VARCHAR(20) | Priority level |

### Issues Table
| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER | Primary key |
| review_id | INTEGER | Foreign key to reviews |
| category | VARCHAR(100) | Issue category |
| severity | VARCHAR(20) | Severity level |
| description | TEXT | Issue description |
| location | VARCHAR(255) | Location in document |
| suggestion | TEXT | Fix suggestion |

---

## Security Features

1. **Password Hashing**: bcrypt with salt
2. **JWT Authentication**: Secure token-based sessions
3. **Authorization**: Users can only access their own reports
4. **Input Validation**: Pydantic schemas validate all inputs
5. **File Validation**: Type and size checking before processing
6. **Environment Variables**: Sensitive data not in code
7. **CORS**: Configured for specific origins

---

## Troubleshooting

### Backend won't start
- Check Python version (3.9+)
- Ensure all dependencies are installed
- Check .env file configuration

### Frontend can't connect to backend
- Verify backend is running on port 8000
- Check VITE_API_URL in frontend/.env
- Check CORS_ORIGINS in backend/.env

### File upload fails
- Check file size (max 10MB)
- Check file type (pdf, docx, txt only)
- Check uploads directory permissions

### AI analysis not working
- In demo mode: Analysis will still work with simulated results
- In production mode: Ensure OPENAI_API_KEY is set correctly
- Check API key has sufficient quota

### "No text could be extracted"
- PDF may be scanned images (requires OCR)
- DOCX may have text in images
- TXT may have unsupported encoding

---

## Project Structure Details

### Backend Modules

1. **app/main.py** - FastAPI app initialization, CORS, routes
2. **app/core/config.py** - Settings management with pydantic-settings
3. **app/core/security.py** - JWT and password hashing utilities
4. **app/core/dependencies.py** - FastAPI dependency functions
5. **app/db/session.py** - Database connection and session management
6. **app/models/** - SQLAlchemy ORM models
7. **app/schemas/** - Pydantic request/response schemas
8. **app/api/auth.py** - Authentication endpoints
9. **app/api/upload.py** - File upload and status endpoints
10. **app/api/reports.py** - Report management endpoints
11. **app/api/reviews.py** - Review and analysis endpoints
12. **app/api/chat.py** - Chat endpoints
13. **app/services/file_extractor.py** - Text extraction logic
14. **app/services/ai_service.py** - OpenAI API integration
15. **app/services/demo_service.py** - Demo mode simulations

### Frontend Modules

1. **src/App.jsx** - Main app with routing
2. **src/App.css** - Global styles
3. **src/services/api.js** - Axios API client
4. **src/context/AuthContext.jsx** - Authentication state
5. **src/hooks/useReports.js** - Custom hooks for data fetching
6. **src/pages/Dashboard.jsx** - Main dashboard
7. **src/pages/Login.jsx** - Login page
8. **src/pages/Register.jsx** - Registration page
9. **src/pages/Upload.jsx** - File upload page
10. **src/pages/Reports.jsx** - Reports list
11. **src/pages/ReportReview.jsx** - Review display
12. **src/pages/Chat.jsx** - AI chat interface

---

## Viva/Project Defense Guide

### Key Points to Explain

1. **System Architecture**
   - Client-server architecture with React frontend and FastAPI backend
   - RESTful API design
   - SQLite database with SQLAlchemy ORM

2. **AI Integration**
   - OpenAI GPT models for natural language understanding
   - Prompt engineering for structured outputs
   - Document chunking for large files
   - Demo mode for testing without API costs

3. **Text Extraction**
   - pdfplumber for PDF parsing
   - python-docx for Word documents
   - Encoding detection for text files

4. **Security**
   - bcrypt password hashing
   - JWT authentication
   - User authorization (data isolation)
   - Input validation

5. **Analysis Categories**
   - Grammar and language
   - Content quality
   - Structure and organization
   - Clarity and readability
   - Academic writing style

---

## License

This project is created for educational purposes as a final year college project.

---

## Acknowledgments

- **OpenAI** - For providing the GPT API
- **FastAPI** - Modern Python web framework
- **React** - Frontend library
- **pdfplumber** - PDF text extraction
- **python-docx** - DOCX file processing
