import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider, useAuth } from './context/AuthContext';
import { Dashboard } from './pages/Dashboard';
import { Login } from './pages/Login';
import { Register } from './pages/Register';
import { Upload } from './pages/Upload';
import { Reports } from './pages/Reports';
import { ReportReview } from './pages/ReportReview';
import { Chat } from './pages/Chat';
import './App.css';

function ProtectedRoute({ children }) {
  const { isAuthenticated, loading } = useAuth();

  if (loading) {
    return <div className="loading-text">Loading...</div>;
  }

  if (!isAuthenticated) {
    return <Navigate to="/login" replace />;
  }

  return children;
}

function PublicRoute({ children }) {
  const { isAuthenticated, loading } = useAuth();

  if (loading) {
    return <div className="loading-text">Loading...</div>;
  }

  if (isAuthenticated) {
    return <Navigate to="/dashboard" replace />;
  }

  return children;
}

function AppRoutes() {
  return (
    <Routes>
      <Route path="/" element={<LandingPage />} />
      <Route path="/login" element={<PublicRoute><Login /></PublicRoute>} />
      <Route path="/register" element={<PublicRoute><Register /></PublicRoute>} />
      <Route path="/dashboard" element={<ProtectedRoute><Dashboard /></ProtectedRoute>} />
      <Route path="/upload" element={<ProtectedRoute><Upload /></ProtectedRoute>} />
      <Route path="/reports" element={<ProtectedRoute><Reports /></ProtectedRoute>} />
      <Route path="/reports/:id/review" element={<ProtectedRoute><ReportReview /></ProtectedRoute>} />
      <Route path="/reports/:id/chat" element={<ProtectedRoute><Chat /></ProtectedRoute>} />
      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  );
}

function LandingPage() {
  return (
    <div className="landing">
      <nav className="landing-nav">
        <a href="/" className="logo">
          <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <path d="M12 2L2 7l10 5 10-5-10-5z" />
            <path d="M2 17l10 5 10-5" />
            <path d="M2 12l10 5 10-5" />
          </svg>
          ReportReviewer
        </a>
        <div className="nav-links">
          <a href="#features">Features</a>
          <a href="#how-it-works">How It Works</a>
          <a href="/login">Login</a>
          <a href="/register" className="btn btn-primary btn-sm">Get Started</a>
        </div>
      </nav>

      <section className="landing-hero">
        <div className="landing-hero-content">
          <h1>
            AI-Powered Project Report<br />
            <span>Reviewer & Improvement Assistant</span>
          </h1>
          <p>
            Upload your academic or project report and let Generative AI analyze it,
            identify problems, provide detailed feedback, and help you improve your work.
          </p>
          <div style={{ display: 'flex', justifyContent: 'center' }}>
            <a href="/register" className="btn btn-primary btn-lg">Get Started Free</a>
            <a href="/login" className="btn btn-lg" style={{ background: 'rgba(255,255,255,0.1)', color: 'white' }}>Login</a>
          </div>
        </div>
      </section>

      <section className="landing-features" id="features">
        <h2>Powerful AI Features</h2>
        <div className="landing-features-grid">
          <div className="landing-feature-card">
            <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <circle cx="11" cy="11" r="8" />
              <path d="m21 21-4.35-4.35" />
            </svg>
            <h3>AI Report Analysis</h3>
            <p>Comprehensive analysis of your report using advanced Generative AI models.</p>
          </div>
          <div className="landing-feature-card">
            <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <path d="M12 20h9" />
              <path d="M16.5 3.5a2.121 2.121 0 0 1 3 3L7 19l-4 1 1-4L16.5 3.5z" />
            </svg>
            <h3>Grammar & Language Review</h3>
            <p>Identify grammar mistakes, spelling errors, and language quality issues.</p>
          </div>
          <div className="landing-feature-card">
            <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <rect x="3" y="3" width="18" height="18" rx="2" />
              <path d="M3 9h18" />
              <path d="M9 21V9" />
            </svg>
            <h3>Section-wise Evaluation</h3>
            <p>Detailed scores and feedback for each section of your report.</p>
          </div>
          <div className="landing-feature-card">
            <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <path d="M12 20h9" />
              <path d="M16.5 3.5a2.121 2.121 0 0 1 3 3L7 19l-4 1 1-4L16.5 3.5z" />
            </svg>
            <h3>AI Improvement Assistant</h3>
            <p>Select any section and let AI rewrite, improve, or expand your content.</p>
          </div>
          <div className="landing-feature-card">
            <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z" />
              <path d="M14 2v6h6" />
              <path d="M16 13H8" />
              <path d="M16 17H8" />
              <path d="M10 9H8" />
            </svg>
            <h3>Detailed Scoring</h3>
            <p>Get overall and category-wise scores with actionable recommendations.</p>
          </div>
          <div className="landing-feature-card">
            <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z" />
            </svg>
            <h3>AI Chat Assistant</h3>
            <p>Ask questions about your report and get AI-powered suggestions.</p>
          </div>
        </div>
      </section>

      <section className="landing-how-it-works" id="how-it-works">
        <h2>How It Works</h2>
        <div className="steps-container">
          <div className="step">
            <div className="step-number">1</div>
            <h3>Upload Report</h3>
            <p>Upload your PDF, DOCX, or TXT report file securely.</p>
          </div>
          <div className="step">
            <div className="step-number">2</div>
            <h3>AI Analyzes</h3>
            <p>Our AI extracts and analyzes your report content.</p>
          </div>
          <div className="step">
            <div className="step-number">3</div>
            <h3>Get Review</h3>
            <p>Receive detailed feedback and scores.</p>
          </div>
          <div className="step">
            <div className="step-number">4</div>
            <h3>Improve</h3>
            <p>Use AI to improve weak sections.</p>
          </div>
          <div className="step">
            <div className="step-number">5</div>
            <h3>Download</h3>
            <p>Export your improved report.</p>
          </div>
        </div>
      </section>

      <footer style={{ padding: '30px 40px', textAlign: 'center', color: 'rgba(255,255,255,0.5)', fontSize: '0.9rem' }}>
        <p>AI-Powered Project Report Reviewer - Final Year College Project</p>
      </footer>
    </div>
  );
}

function App() {
  return (
    <BrowserRouter>
      <AuthProvider>
        <AppRoutes />
      </AuthProvider>
    </BrowserRouter>
  );
}

export default App;
