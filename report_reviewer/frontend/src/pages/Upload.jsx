import { useState, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import { useUpload } from '../hooks/useReports';
import { Upload as UploadIcon, FileText, X, CheckCircle, AlertCircle, File } from 'lucide-react';

export function Upload() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [dragActive, setDragActive] = useState(false);
  const fileInputRef = useRef(null);
  const { uploading, progress, error, uploadedReport, uploadFile } = useUpload();
  const navigate = useNavigate();

  const handleDrag = (e) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === 'dragenter' || e.type === 'dragover') {
      setDragActive(true);
    } else if (e.type === 'dragleave') {
      setDragActive(false);
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);

    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      checkAndSetFile(e.dataTransfer.files[0]);
    }
  };

  const handleFileChange = (e) => {
    if (e.target.files && e.target.files[0]) {
      checkAndSetFile(e.target.files[0]);
    }
  };

  const checkAndSetFile = (file) => {
    // Validate file type
    const allowedTypes = ['application/pdf', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document', 'text/plain'];
    const allowedExtensions = ['pdf', 'docx', 'txt'];

    const fileExtension = file.name.split('.').pop().toLowerCase();

    if (!allowedExtensions.includes(fileExtension)) {
      alert(`File type not supported. Please upload PDF, DOCX, or TXT files.`);
      return;
    }

    // Validate file size (10MB limit)
    const maxSize = 10 * 1024 * 1024; // 10MB
    if (file.size > maxSize) {
      alert('File is too large. Maximum size is 10MB.');
      return;
    }

    setSelectedFile(file);
  };

  const handleUpload = async () => {
    if (!selectedFile) return;

    const result = await uploadFile(selectedFile);

    if (result.success) {
      // Redirect to reports page or show success
      alert('Report uploaded successfully! You can track its status in My Reports.');
      navigate('/reports');
    }
  };

  const removeFile = () => {
    setSelectedFile(null);
    if (fileInputRef.current) {
      fileInputRef.current.value = '';
    }
  };

  const formatFileSize = (bytes) => {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  };

  return (
    <div style={{ minHeight: '100vh', background: 'var(--gray-100)', padding: '30px 40px' }}>
      {/* Sidebar */}
      <aside className="sidebar">
        <div className="sidebar-header">
          <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
            <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="var(--primary)" strokeWidth="2">
              <path d="M12 2L2 7l10 5 10-5-10-5z" />
              <path d="M2 17l10 5 10-5" />
              <path d="M2 12l10 5 10-5" />
            </svg>
            <h2>ReportReviewer</h2>
          </div>
        </div>

        <nav className="sidebar-nav">
          <a href="/dashboard" className="sidebar-nav-item">
            <FileText size={20} />
            Dashboard
          </a>
          <a href="/upload" className="sidebar-nav-item active">
            <UploadIcon size={20} />
            Upload Report
          </a>
          <a href="/reports" className="sidebar-nav-item">
            <FileText size={20} />
            My Reports
          </a>
        </nav>

        <div className="sidebar-footer">
          <a href="/dashboard" style={{
            display: 'flex',
            alignItems: 'center',
            gap: '12px',
            padding: '10px 24px',
            color: 'rgba(255,255,255,0.7)',
            textDecoration: 'none',
            fontSize: '0.95rem'
          }}>
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4" />
              <polyline points="16 17 21 12 16 7" />
              <line x1="21" y1="12" x2="9" y2="12" />
            </svg>
            Logout
          </a>
        </div>
      </aside>

      {/* Main Content */}
      <main className="main-content">
        <div className="page-header">
          <h1>Upload Report</h1>
          <p style={{ color: 'var(--gray-600)' }}>
            Upload your project report for AI-powered analysis
          </p>
        </div>

        <div style={{ display: 'grid', gridTemplateColumns: '1fr 300px', gap: '30px', alignItems: 'start' }}>
          {/* Upload Area */}
          <div className="card">
            <div
              className={`upload-area ${dragActive ? 'dragover' : ''}`}
              onDragEnter={handleDrag}
              onDragLeave={handleDrag}
              onDragOver={handleDrag}
              onDrop={handleDrop}
              onClick={() => fileInputRef.current?.click()}
            >
              <input
                ref={fileInputRef}
                type="file"
                id="file-upload"
                className="hidden"
                onChange={handleFileChange}
                accept=".pdf,.docx,.txt"
              />

              {!selectedFile ? (
                <>
                  <UploadIcon size={64} />
                  <h3>Drag & Drop your file here</h3>
                  <p>or click to browse</p>
                  <p style={{ marginTop: '16px', fontSize: '0.85rem', color: 'var(--gray-500)' }}>
                    Supported formats: PDF, DOCX, TXT (max 10MB)
                  </p>
                </>
              ) : (
                <div style={{ padding: '20px' }}>
                  <div style={{
                    display: 'flex',
                    alignItems: 'center',
                    gap: '16px',
                    padding: '16px',
                    background: 'var(--white)',
                    borderRadius: 'var(--radius)',
                    border: '1px solid var(--gray-200)'
                  }}>
                    <div style={{
                      width: '56px',
                      height: '56px',
                      borderRadius: '8px',
                      background: 'var(--primary-light)',
                      display: 'flex',
                      alignItems: 'center',
                      justifyContent: 'center',
                      color: 'var(--primary)'
                    }}>
                      <File size={28} />
                    </div>
                    <div style={{ flex: 1, minWidth: 0 }}>
                      <p style={{ fontWeight: 600, marginBottom: '4px', whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis' }}>
                        {selectedFile.name}
                      </p>
                      <p style={{ color: 'var(--gray-600)', fontSize: '0.9rem' }}>
                        {formatFileSize(selectedFile.size)}
                      </p>
                    </div>
                    <button
                      className="btn btn-secondary btn-sm"
                      onClick={(e) => {
                        e.stopPropagation();
                        removeFile();
                      }}
                    >
                      <X size={16} />
                    </button>
                  </div>
                </div>
              )}
            </div>

            {/* File Info */}
            {selectedFile && !uploading && (
              <div style={{ marginTop: '20px', padding: '16px', background: 'var(--gray-50)', borderRadius: 'var(--radius)' }}>
                <h4 style={{ marginBottom: '12px', fontSize: '1rem' }}>File Details</h4>
                <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '12px', fontSize: '0.9rem' }}>
                  <div>
                    <span style={{ color: 'var(--gray-600)' }}>Name:</span>
                    <span style={{ marginLeft: '8px', fontWeight: 500 }}>{selectedFile.name}</span>
                  </div>
                  <div>
                    <span style={{ color: 'var(--gray-600)' }}>Size:</span>
                    <span style={{ marginLeft: '8px', fontWeight: 500 }}>{formatFileSize(selectedFile.size)}</span>
                  </div>
                  <div>
                    <span style={{ color: 'var(--gray-600)' }}>Type:</span>
                    <span style={{ marginLeft: '8px', fontWeight: 500, textTransform: 'uppercase' }}>
                      {selectedFile.name.split('.').pop()}
                    </span>
                  </div>
                </div>
              </div>
            )}

            {/* Upload Error */}
            {error && (
              <div className="alert alert-error" style={{ marginTop: '20px' }}>
                <AlertCircle size={20} />
                {error}
              </div>
            )}

            {/* Upload Button */}
            {selectedFile && !uploading && (
              <button
                className="btn btn-primary btn-lg"
                style={{ width: '100%', marginTop: '20px' }}
                onClick={handleUpload}
              >
                <UploadIcon size={20} />
                Upload and Analyze
              </button>
            )}

            {/* Uploading Progress */}
            {uploading && (
              <div style={{ marginTop: '20px' }}>
                <div style={{
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'space-between',
                  marginBottom: '8px'
                }}>
                  <span style={{ fontWeight: 500 }}>Uploading...</span>
                  <span style={{ color: 'var(--gray-600)', fontSize: '0.9rem' }}>
                    {progress}%
                  </span>
                </div>
                <div style={{
                  width: '100%',
                  height: '8px',
                  background: 'var(--gray-200)',
                  borderRadius: '4px',
                  overflow: 'hidden'
                }}>
                  <div style={{
                    width: `${progress}%`,
                    height: '100%',
                    background: 'var(--primary)',
                    borderRadius: '4px',
                    transition: 'width 0.3s ease'
                  }} />
                </div>
                <p style={{ fontSize: '0.85rem', color: 'var(--gray-600)', marginTop: '8px' }}>
                  Please wait while we process your file...
                </p>
              </div>
            )}
          </div>

          {/* Supported Formats Info */}
          <div className="card">
            <h3 style={{ marginBottom: '20px' }}>Supported Formats</h3>

            <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
              <div style={{
                display: 'flex',
                alignItems: 'center',
                gap: '12px',
                padding: '12px',
                background: 'var(--gray-50)',
                borderRadius: 'var(--radius)'
              }}>
                <div style={{
                  width: '40px',
                  height: '40px',
                  borderRadius: '8px',
                  background: '#ff6b6b',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  color: 'white',
                  fontWeight: 700,
                  fontSize: '0.85rem'
                }}>
                  PDF
                </div>
                <div>
                  <p style={{ fontWeight: 500, marginBottom: '2px' }}>PDF Documents</p>
                  <p style={{ fontSize: '0.85rem', color: 'var(--gray-600)' }}>Text-based PDFs</p>
                </div>
              </div>

              <div style={{
                display: 'flex',
                alignItems: 'center',
                gap: '12px',
                padding: '12px',
                background: 'var(--gray-50)',
                borderRadius: 'var(--radius)'
              }}>
                <div style={{
                  width: '40px',
                  height: '40px',
                  borderRadius: '8px',
                  background: '#4cc9f0',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  color: 'white',
                  fontWeight: 700,
                  fontSize: '0.75rem'
                }}>
                  DOCX
                </div>
                <div>
                  <p style={{ fontWeight: 500, marginBottom: '2px' }}>Word Documents</p>
                  <p style={{ fontSize: '0.85rem', color: 'var(--gray-600)' }}>DOCX format</p>
                </div>
              </div>

              <div style={{
                display: 'flex',
                alignItems: 'center',
                gap: '12px',
                padding: '12px',
                background: 'var(--gray-50)',
                borderRadius: 'var(--radius)'
              }}>
                <div style={{
                  width: '40px',
                  height: '40px',
                  borderRadius: '8px',
                  background: 'var(--success)',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  color: 'white',
                  fontWeight: 700,
                  fontSize: '0.85rem'
                }}>
                  TXT
                </div>
                <div>
                  <p style={{ fontWeight: 500, marginBottom: '2px' }}>Plain Text</p>
                  <p style={{ fontSize: '0.85rem', color: 'var(--gray-600)' }}>TXT format</p>
                </div>
              </div>
            </div>

            <div className="demo-banner" style={{ marginTop: '20px' }}>
              <AlertCircle size={20} />
              <div>
                <strong>Demo Mode Notice:</strong>
                <br />
                <span style={{ fontSize: '0.85rem' }}>
                  Without an OpenAI API key, analysis will run in demo mode with simulated results.
                </span>
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}
