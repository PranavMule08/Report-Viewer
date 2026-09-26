import { useEffect, useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { useReports } from '../hooks/useReports';
import { reportAPI } from '../services/api';
import { FileText, Clock, CheckCircle, XCircle, AlertCircle, Trash2, Eye, Upload } from 'lucide-react';

export function Reports() {
  const { reports, loading, error, refetch } = useReports();
  const [deletingId, setDeletingId] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    refetch();
  }, [refetch]);

  const handleDelete = async (id) => {
    if (!confirm('Are you sure you want to delete this report? This action cannot be undone.')) {
      return;
    }

    setDeletingId(id);
    try {
      await reportAPI.delete(id);
      refetch();
    } catch (err) {
      alert(err.response?.data?.detail || 'Failed to delete report');
    } finally {
      setDeletingId(null);
    }
  };

  const formatDate = (date) => {
    return new Date(date).toLocaleDateString('en-US', {
      month: 'short',
      day: 'numeric',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
    });
  };

  const formatFileSize = (bytes) => {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  };

  const getStatusBadge = (status) => {
    switch (status) {
      case 'completed':
        return <span className="badge badge-success"><CheckCircle size={14} /> Completed</span>;
      case 'processing':
        return <span className="badge badge-warning"><Clock size={14} /> Processing</span>;
      case 'uploaded':
        return <span className="badge badge-info">Uploaded</span>;
      case 'failed':
        return <span className="badge badge-danger"><XCircle size={14} /> Failed</span>;
      default:
        return <span className="badge badge-neutral">{status}</span>;
    }
  };

  const getScoreColor = (score) => {
    if (!score) return 'var(--gray-400)';
    if (score >= 80) return 'var(--success)';
    if (score >= 60) return 'var(--warning)';
    return 'var(--danger)';
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
          <a href="/upload" className="sidebar-nav-item">
            <Upload size={20} />
            Upload Report
          </a>
          <a href="/reports" className="sidebar-nav-item active">
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
          <div>
            <h1>My Reports</h1>
            <p style={{ color: 'var(--gray-600)' }}>
              View and manage all your uploaded reports
            </p>
          </div>
          <Link to="/upload" className="btn btn-primary">
            <Upload size={18} />
            Upload New
          </Link>
        </div>

        {error && (
          <div className="alert alert-error">
            <AlertCircle size={20} />
            {error}
          </div>
        )}

        {loading ? (
          <div style={{ textAlign: 'center', padding: '60px' }}>
            <div className="spinner" />
            <p className="loading-text">Loading reports...</p>
          </div>
        ) : reports && reports.length > 0 ? (
          <div className="card">
            <div className="table-container">
              <table className="table">
                <thead>
                  <tr>
                    <th>Report Name</th>
                    <th>Type</th>
                    <th>Size</th>
                    <th>Upload Date</th>
                    <th>Status</th>
                    <th>Score</th>
                    <th>Actions</th>
                  </tr>
                </thead>
                <tbody>
                  {reports.map((report) => (
                    <tr key={report.id}>
                      <td>
                        <Link
                          to={`/reports/${report.id}/review`}
                          style={{ color: 'var(--primary)', textDecoration: 'none', fontWeight: 500 }}
                        >
                          <FileText size={16} style={{ marginRight: '8px', verticalAlign: 'middle' }} />
                          {report.original_filename}
                        </Link>
                      </td>
                      <td>
                        <span style={{
                          padding: '2px 8px',
                          borderRadius: '4px',
                          background: 'var(--gray-100)',
                          fontSize: '0.8rem',
                          textTransform: 'uppercase',
                          fontWeight: 500
                        }}>
                          {report.file_type}
                        </span>
                      </td>
                      <td>{formatFileSize(report.file_size)}</td>
                      <td>{formatDate(report.upload_date)}</td>
                      <td>{getStatusBadge(report.status)}</td>
                      <td>
                        {report.overall_score !== null && report.overall_score !== undefined ? (
                          <span style={{ fontWeight: 600, color: getScoreColor(report.overall_score) }}>
                            {report.overall_score.toFixed(0)}/100
                          </span>
                        ) : (
                          <span style={{ color: 'var(--gray-400)' }}>-</span>
                        )}
                      </td>
                      <td>
                        <div style={{ display: 'flex', gap: '8px' }}>
                          {report.status === 'completed' && report.overall_score !== null && (
                            <Link to={`/reports/${report.id}/review`} className="btn btn-sm btn-primary">
                              <Eye size={14} />
                              View
                            </Link>
                          )}
                          {report.status === 'completed' && (
                            <Link to={`/reports/${report.id}/chat`} className="btn btn-sm btn-secondary">
                              Chat
                            </Link>
                          )}
                          <button
                            className="btn btn-sm btn-danger"
                            onClick={() => handleDelete(report.id)}
                            disabled={deletingId === report.id}
                          >
                            <Trash2 size={14} />
                            {deletingId === report.id ? '...' : 'Delete'}
                          </button>
                        </div>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        ) : (
          <div className="card">
            <div className="empty-state">
              <FileText size={64} />
              <h3>No reports found</h3>
              <p>You haven't uploaded any reports yet</p>
              <Link to="/upload" className="btn btn-primary">
                <Upload size={18} />
                Upload Your First Report
              </Link>
            </div>
          </div>
        )}
      </main>
    </div>
  );
}
