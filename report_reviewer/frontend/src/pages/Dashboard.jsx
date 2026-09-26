import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { useDashboard } from '../hooks/useReports';
import {
  FileText,
  Clock,
  BarChart3,
  ArrowUpRight,
  Upload,
  File,
  RefreshCw,
  AlertTriangle
} from 'lucide-react';
import { Link } from 'react-router-dom';

export function Dashboard() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();
  const { dashboard, loading, error, refetch } = useDashboard();
  const [refreshing, setRefreshing] = useState(false);

  useEffect(() => {
    refetch();
  }, [refetch]);

  const handleRefresh = async () => {
    setRefreshing(true);
    await refetch();
    setRefreshing(false);
  };

  const formatDate = (date) => {
    return new Date(date).toLocaleDateString('en-US', {
      month: 'short',
      day: 'numeric',
      year: 'numeric',
    });
  };

  const getStatusBadge = (status) => {
    switch (status) {
      case 'completed':
        return <span className="badge badge-success">Completed</span>;
      case 'processing':
        return <span className="badge badge-warning">Processing</span>;
      case 'uploaded':
        return <span className="badge badge-info">Uploaded</span>;
      case 'failed':
        return <span className="badge badge-danger">Failed</span>;
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
    <div style={{ minHeight: '100vh', background: 'var(--gray-100)' }}>
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
          <Link to="/dashboard" className="sidebar-nav-item active">
            <BarChart3 size={20} />
            Dashboard
          </Link>
          <Link to="/upload" className="sidebar-nav-item">
            <Upload size={20} />
            Upload Report
          </Link>
          <Link to="/reports" className="sidebar-nav-item">
            <FileText size={20} />
            My Reports
          </Link>
        </nav>

        <div className="sidebar-footer">
          <div style={{ marginBottom: '16px', padding: '0 24px' }}>
            <div style={{ fontSize: '0.85rem', color: 'rgba(255,255,255,0.5)' }}>
              {user?.name || 'User'}
            </div>
            <div style={{ fontSize: '0.75rem', color: 'rgba(255,255,255,0.3)' }}>
              {user?.email}
            </div>
          </div>
          <button onClick={logout}>
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4" />
              <polyline points="16 17 21 12 16 7" />
              <line x1="21" y1="12" x2="9" y2="12" />
            </svg>
            Logout
          </button>
        </div>
      </aside>

      {/* Main Content */}
      <main className="main-content" style={{ padding: '30px 40px' }}>
        <div className="page-header">
          <div>
            <h1>Dashboard</h1>
            <p style={{ color: 'var(--gray-600)' }}>Welcome back, {user?.name || 'User'}!</p>
          </div>
          <div style={{ display: 'flex', gap: '12px' }}>
            <button className="btn btn-secondary" onClick={handleRefresh} disabled={refreshing}>
              <RefreshCw size={18} style={{ animation: refreshing ? 'spin 1s linear infinite' : 'none' }} />
              Refresh
            </button>
            <Link to="/upload" className="btn btn-primary">
              <Upload size={18} />
              Quick Upload
            </Link>
          </div>
        </div>

        {error && (
          <div className="alert alert-error">
            <AlertTriangle size={20} />
            {error}
          </div>
        )}

        {loading && !dashboard ? (
          <div style={{ textAlign: 'center', padding: '60px' }}>
            <div className="spinner" />
            <p className="loading-text">Loading dashboard...</p>
          </div>
        ) : dashboard ? (
          <>
            {/* Stats Grid */}
            <div className="grid grid-4" style={{ marginBottom: '30px' }}>
              <div className="card">
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
                  <div>
                    <p style={{ color: 'var(--gray-600)', fontSize: '0.9rem', marginBottom: '8px' }}>
                      Total Reports
                    </p>
                    <h3 style={{ fontSize: '2rem', margin: 0 }}>{dashboard.total_reports}</h3>
                  </div>
                  <div style={{
                    width: '48px',
                    height: '48px',
                    borderRadius: '12px',
                    background: 'var(--primary-light)',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    color: 'var(--primary)'
                  }}>
                    <FileText size={24} />
                  </div>
                </div>
              </div>

              <div className="card">
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
                  <div>
                    <p style={{ color: 'var(--gray-600)', fontSize: '0.9rem', marginBottom: '8px' }}>
                      Processing
                    </p>
                    <h3 style={{ fontSize: '2rem', margin: 0, color: 'var(--warning)' }}>
                      {dashboard.processing_reports}
                    </h3>
                  </div>
                  <div style={{
                    width: '48px',
                    height: '48px',
                    borderRadius: '12px',
                    background: '#fff3cd',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    color: '#856404'
                  }}>
                    <Clock size={24} />
                  </div>
                </div>
              </div>

              <div className="card">
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
                  <div>
                    <p style={{ color: 'var(--gray-600)', fontSize: '0.9rem', marginBottom: '8px' }}>
                      Completed
                    </p>
                    <h3 style={{ fontSize: '2rem', margin: 0, color: 'var(--success)' }}>
                      {dashboard.completed_reports}
                    </h3>
                  </div>
                  <div style={{
                    width: '48px',
                    height: '48px',
                    borderRadius: '12px',
                    background: '#d4edda',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    color: '#155724'
                  }}>
                    <File size={24} />
                  </div>
                </div>
              </div>

              <div className="card">
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
                  <div>
                    <p style={{ color: 'var(--gray-600)', fontSize: '0.9rem', marginBottom: '8px' }}>
                      Average Score
                    </p>
                    <h3 style={{
                      fontSize: '2rem',
                      margin: 0,
                      color: getScoreColor(dashboard.average_score)
                    }}>
                      {dashboard.average_score !== null && dashboard.average_score !== undefined
                        ? dashboard.average_score.toFixed(1)
                        : '-'}
                    </h3>
                  </div>
                  <div style={{
                    width: '48px',
                    height: '48px',
                    borderRadius: '12px',
                    background: 'var(--secondary)',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    color: 'white'
                  }}>
                    <BarChart3 size={24} />
                  </div>
                </div>
              </div>
            </div>

            {/* Recent Reports */}
            <div className="card">
              <div className="card-header">
                <h3 className="card-title">Recent Reports</h3>
                <Link to="/reports" className="btn btn-sm btn-secondary">
                  View All
                  <ArrowUpRight size={16} />
                </Link>
              </div>

              {dashboard.recent_reports && dashboard.recent_reports.length > 0 ? (
                <div className="table-container">
                  <table className="table">
                    <thead>
                      <tr>
                        <th>Report Name</th>
                        <th>Type</th>
                        <th>Upload Date</th>
                        <th>Status</th>
                        <th>Score</th>
                        <th></th>
                      </tr>
                    </thead>
                    <tbody>
                      {dashboard.recent_reports.map((report) => (
                        <tr key={report.id}>
                          <td>
                            <Link
                              to={`/reports/${report.id}/review`}
                              style={{ color: 'var(--primary)', textDecoration: 'none', fontWeight: 500 }}
                            >
                              {report.original_filename}
                            </Link>
                          </td>
                          <td>
                            <span style={{
                              padding: '2px 8px',
                              borderRadius: '4px',
                              background: 'var(--gray-100)',
                              fontSize: '0.8rem',
                              textTransform: 'uppercase'
                            }}>
                              {report.file_type}
                            </span>
                          </td>
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
                            {report.status === 'completed' && report.overall_score !== null && (
                              <Link
                                to={`/reports/${report.id}/review`}
                                className="btn btn-sm btn-primary"
                              >
                                View Review
                              </Link>
                            )}
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              ) : (
                <div className="empty-state">
                  <FileText size={64} />
                  <h3>No reports yet</h3>
                  <p>Upload your first report to get started</p>
                  <Link to="/upload" className="btn btn-primary">
                    <Upload size={18} />
                    Upload Report
                  </Link>
                </div>
              )}
            </div>
          </>
        ) : (
          <div className="card">
            <div className="empty-state">
              <BarChart3 size={64} />
              <h3>Unable to load dashboard</h3>
              <p>Please try refreshing the page</p>
              <button className="btn btn-primary" onClick={handleRefresh}>
                <RefreshCw size={18} />
                Try Again
              </button>
            </div>
          </div>
        )}
      </main>
    </div>
  );
}
