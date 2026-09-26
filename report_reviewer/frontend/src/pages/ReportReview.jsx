import { useEffect, useState, useRef } from 'react';
import { useParams, useNavigate, Link } from 'react-router-dom';
import { useReview } from '../hooks/useReports';
import { Chat } from './Chat';
import {
  ArrowLeft,
  CheckCircle,
  XCircle,
  AlertTriangle,
  Lightbulb,
  ThumbsUp,
  ThumbsDown,
  Clock,
  FileText,
  ShieldAlert
} from 'lucide-react';
import { BarChart3 } from 'lucide-react';

export function ReportReview() {
  const { id } = useParams();
  const navigate = useNavigate();
  const { review, sections, issues, analyzing, error, demoMode, analyzeReport, refetchReview } = useReview(id);
  const [activeTab, setActiveTab] = useState('overview');
  const [copiedText, setCopiedText] = useState(null);
  const [categoryFilter, setCategoryFilter] = useState(null);
  const autoAnalyzeTriggered = useRef(false);

  useEffect(() => {
    // Auto-analyze once when no review exists yet
    if (review === null && !autoAnalyzeTriggered.current) {
      autoAnalyzeTriggered.current = true;
      analyzeReport();
    }
  }, [review, analyzeReport]);

  const formatDate = (date) => {
    return new Date(date).toLocaleDateString('en-US', {
      month: 'long',
      day: 'numeric',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
    });
  };

  const getScoreColor = (score) => {
    if (!score) return 'var(--gray-400)';
    if (score >= 80) return 'var(--success)';
    if (score >= 60) return 'var(--warning)';
    return 'var(--danger)';
  };

  const getScoreBadgeClass = (score) => {
    if (!score) return 'badge-neutral';
    if (score >= 80) return 'badge-success';
    if (score >= 60) return 'badge-warning';
    return 'badge-danger';
  };

  const getSeverityBadge = (severity) => {
    switch (severity) {
      case 'critical':
        return <span className="issue-severity critical">Critical</span>;
      case 'high':
        return <span className="issue-severity high">High</span>;
      case 'medium':
        return <span className="issue-severity medium">Medium</span>;
      case 'low':
        return <span className="issue-severity low">Low</span>;
      default:
        return <span className="badge badge-neutral">{severity}</span>;
    }
  };

  const copyToClipboard = (text) => {
    navigator.clipboard.writeText(text);
    setCopiedText(text);
    setTimeout(() => setCopiedText(null), 2000);
  };

  const filteredIssues = (category) => {
    if (!category) return issues;
    return issues.filter(issue => issue.category === category);
  };

  const categories = ['all', ...new Set(issues.map(i => i.category))];

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
          <Link to="/dashboard" className="sidebar-nav-item">
            <BarChart3 size={20} />
            Dashboard
          </Link>
          <Link to="/upload" className="sidebar-nav-item">
            <FileText size={20} />
            Upload Report
          </Link>
          <Link to="/reports" className="sidebar-nav-item">
            <FileText size={20} />
            My Reports
          </Link>
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
      <main className="main-content" style={{ padding: '30px 40px' }}>
        <Link to="/reports" style={{
          display: 'inline-flex',
          alignItems: 'center',
          gap: '8px',
          color: 'var(--gray-600)',
          textDecoration: 'none',
          fontSize: '0.9rem',
          marginBottom: '16px'
        }}>
          <ArrowLeft size={18} />
          Back to Reports
        </Link>

        {error && !review && (
          <div className="alert alert-error">
            <AlertTriangle size={20} />
            {error}
          </div>
        )}

        {demoMode && (
          <div className="demo-banner">
            <ShieldAlert size={20} />
            <div>
              <strong>Demo Mode:</strong>
              <br />
              <span style={{ fontSize: '0.85rem' }}>
                This analysis was generated in demo mode without a real AI API. Connect an OpenAI API key for genuine AI analysis.
              </span>
            </div>
          </div>
        )}

        {analyzing && !review ? (
          <div style={{ textAlign: 'center', padding: '60px' }}>
            <div className="spinner" />
            <p className="loading-text">AI is analyzing your report...</p>
            <p style={{ color: 'var(--gray-500)', fontSize: '0.9rem' }}>This may take a minute</p>
          </div>
        ) : review ? (
          <>
            {/* Review Header */}
            <div className="review-header" style={{ marginBottom: '30px' }}>
              <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '12px', marginBottom: '16px' }}>
                <FileText size={24} style={{ color: 'var(--gray-600)' }} />
                <span style={{ color: 'var(--gray-600)', fontSize: '1.1rem' }}>
                  {review.id ? `Review #${review.id}` : 'Report Review'}
                </span>
              </div>
              <h1 style={{ marginBottom: '8px' }}>
                {demoMode ? 'Demo Analysis Report' : 'AI-Powered Report Analysis'}
              </h1>
              <p className="review-date">
                Generated on {formatDate(review.created_at)}
              </p>

              {/* Overall Score */}
              <div className="score-display">
                <div className={`score-circle score-${review.overall_score >= 80 ? 'excellent' : review.overall_score >= 60 ? 'good' : 'fair'}`}>
                  <span>{review.overall_score?.toFixed(0)}</span>
                </div>
                <div style={{ textAlign: 'center' }}>
                  <p style={{ fontSize: '1.1rem', fontWeight: 600, marginBottom: '4px' }}>
                    {review.overall_quality || 'Needs Review'}
                  </p>
                  <span className={`badge ${getScoreBadgeClass(review.overall_score)}`} style={{ marginTop: '8px' }}>
                    Overall Score
                  </span>
                </div>
              </div>

              {/* Quick Stats */}
              {review.grammar_score && (
                <div className="score-statistics">
                  <div className="stat-card">
                    <div className="stat-value" style={{ color: getScoreColor(review.grammar_score) }}>
                      {review.grammar_score?.toFixed(0)}
                    </div>
                    <div className="stat-label">Grammar</div>
                  </div>
                  <div className="stat-card">
                    <div className="stat-value" style={{ color: getScoreColor(review.content_score) }}>
                      {review.content_score?.toFixed(0)}
                    </div>
                    <div className="stat-label">Content</div>
                  </div>
                  <div className="stat-card">
                    <div className="stat-value" style={{ color: getScoreColor(review.structure_score) }}>
                      {review.structure_score?.toFixed(0)}
                    </div>
                    <div className="stat-label">Structure</div>
                  </div>
                  <div className="stat-card">
                    <div className="stat-value" style={{ color: getScoreColor(review.clarity_score) }}>
                      {review.clarity_score?.toFixed(0)}
                    </div>
                    <div className="stat-label">Clarity</div>
                  </div>
                  <div className="stat-card">
                    <div className="stat-value" style={{ color: getScoreColor(review.academic_style_score) }}>
                      {review.academic_style_score?.toFixed(0)}
                    </div>
                    <div className="stat-label">Academic Style</div>
                  </div>
                  <div className="stat-card">
                    <div className="stat-value">
                      {sections?.length || 0}
                    </div>
                    <div className="stat-label">Sections Analyzed</div>
                  </div>
                </div>
              )}
            </div>

            {/* Tabs */}
            <div className="tabs">
              <button
                className={`tab ${activeTab === 'overview' ? 'active' : ''}`}
                onClick={() => setActiveTab('overview')}
              >
                Overview
              </button>
              <button
                className={`tab ${activeTab === 'sections' ? 'active' : ''}`}
                onClick={() => setActiveTab('sections')}
              >
                Sections ({sections?.length || 0})
              </button>
              <button
                className={`tab ${activeTab === 'issues' ? 'active' : ''}`}
                onClick={() => setActiveTab('issues')}
              >
                Issues ({issues?.length || 0})
              </button>
              <button
                className={`tab ${activeTab === 'chat' ? 'active' : ''}`}
                onClick={() => setActiveTab('chat')}
              >
                AI Chat
              </button>
            </div>

            {/* Tab Content */}
            {activeTab === 'overview' && (
              <div className="grid grid-2">
                {/* Summary */}
                <div className="card">
                  <h3 style={{ marginBottom: '16px' }}>Summary</h3>
                  <p style={{ color: 'var(--gray-700)', lineHeight: 1.7 }}>
                    {review.summary || 'No summary available.'}
                  </p>
                </div>

                {/* Strengths & Weaknesses */}
                <div className="card">
                  <h3 style={{ marginBottom: '16px', color: 'var(--success)' }}>
                    <ThumbsUp size={20} style={{ marginRight: '8px', verticalAlign: 'middle' }} />
                    Strengths
                  </h3>
                  {review.strengths && review.strengths.length > 0 ? (
                    <ul style={{ listStyle: 'none', padding: 0 }}>
                      {review.strengths.map((strength, index) => (
                        <li key={index} style={{
                          padding: '8px 0',
                          paddingLeft: '24px',
                          position: 'relative',
                          borderBottom: '1px solid var(--gray-100)'
                        }}>
                          <span style={{
                            position: 'absolute',
                            left: 0,
                            color: 'var(--success)',
                            fontWeight: 700
                          }}>✓</span>
                          {strength}
                        </li>
                      ))}
                    </ul>
                  ) : (
                    <p style={{ color: 'var(--gray-500)' }}>No strengths identified.</p>
                  )}
                </div>

                {/* Weaknesses */}
                <div className="card">
                  <h3 style={{ marginBottom: '16px', color: 'var(--danger)' }}>
                    <ThumbsDown size={20} style={{ marginRight: '8px', verticalAlign: 'middle' }} />
                    Weaknesses
                  </h3>
                  {review.weaknesses && review.weaknesses.length > 0 ? (
                    <ul style={{ listStyle: 'none', padding: 0 }}>
                      {review.weaknesses.map((weakness, index) => (
                        <li key={index} style={{
                          padding: '8px 0',
                          paddingLeft: '24px',
                          position: 'relative',
                          borderBottom: '1px solid var(--gray-100)'
                        }}>
                          <span style={{
                            position: 'absolute',
                            left: 0,
                            color: 'var(--danger)',
                            fontWeight: 700
                          }}>−</span>
                          {weakness}
                        </li>
                      ))}
                    </ul>
                  ) : (
                    <p style={{ color: 'var(--gray-500)' }}>No weaknesses identified.</p>
                  )}
                </div>

                {/* Recommendations */}
                <div className="card" style={{ gridColumn: '1 / -1' }}>
                  <h3 style={{ marginBottom: '16px', color: 'var(--primary)' }}>
                    <Lightbulb size={20} style={{ marginRight: '8px', verticalAlign: 'middle' }} />
                    Priority Recommendations
                  </h3>
                  {review.recommendations && review.recommendations.length > 0 ? (
                    <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', gap: '16px' }}>
                      {review.recommendations.map((rec, index) => (
                        <div
                          key={index}
                          style={{
                            display: 'flex',
                            alignItems: 'flex-start',
                            gap: '12px',
                            padding: '12px 16px',
                            background: 'var(--gray-50)',
                            borderRadius: 'var(--radius)',
                            borderLeft: '3px solid var(--primary)'
                          }}
                        >
                          <span style={{
                            width: '24px',
                            height: '24px',
                            borderRadius: '50%',
                            background: 'var(--primary)',
                            color: 'white',
                            display: 'flex',
                            alignItems: 'center',
                            justifyContent: 'center',
                            fontSize: '0.85rem',
                            fontWeight: 600,
                            flexShrink: 0
                          }}>
                            {index + 1}
                          </span>
                          <span style={{ color: 'var(--gray-700)' }}>{rec}</span>
                        </div>
                      ))}
                    </div>
                  ) : (
                    <p style={{ color: 'var(--gray-500)' }}>No recommendations available.</p>
                  )}
                </div>
              </div>
            )}

            {activeTab === 'sections' && (
              <div>
                {sections && sections.length > 0 ? (
                  <div className="card">
                    {sections.map((section, index) => (
                      <div
                        key={section.id || index}
                        className={`section-card ${section.priority || 'low'}`}
                      >
                        <div className="section-header">
                          <h4>{section.section_name}</h4>
                          <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
                            <span style={{
                              padding: '4px 12px',
                              borderRadius: '9999px',
                              background: 'var(--gray-200)',
                              fontSize: '0.85rem',
                              fontWeight: 600,
                              color: section.priority === 'critical' ? 'var(--danger)' :
                                    section.priority === 'high' ? '#8b4513' :
                                    section.priority === 'medium' ? '#856404' : '#155724'
                            }}>
                              {section.priority || 'Medium'} Priority
                            </span>
                            <span className="section-score">{section.score?.toFixed(0)}/100</span>
                          </div>
                        </div>

                        {section.content_preview && (
                          <p style={{
                            fontSize: '0.85rem',
                            color: 'var(--gray-600)',
                            marginBottom: '12px',
                            padding: '8px 12px',
                            background: 'var(--gray-100)',
                            borderRadius: 'var(--radius)',
                            fontStyle: 'italic'
                          }}>
                            "{section.content_preview.substring(0, 150)}..."
                          </p>
                        )}

                        <div className="section-content">
                          <div>
                            <h5><CheckCircle size={14} style={{ marginRight: '4px', verticalAlign: 'middle', color: 'var(--success)' }} /> Strengths</h5>
                            <ul>
                              {section.strengths && section.strengths.map((s, i) => (
                                <li key={i}>{s}</li>
                              ))}
                            </ul>
                          </div>
                          <div>
                            <h5><XCircle size={14} style={{ marginRight: '4px', verticalAlign: 'middle', color: 'var(--danger)' }} /> Areas to Improve</h5>
                            <ul>
                              {section.weaknesses && section.weaknesses.map((w, i) => (
                                <li key={i} className="negative">{w}</li>
                              ))}
                            </ul>
                          </div>
                          <div>
                            <h5><Lightbulb size={14} style={{ marginRight: '4px', verticalAlign: 'middle', color: 'var(--primary)' }} /> Suggestions</h5>
                            <ul>
                              {section.suggestions && section.suggestions.map((s, i) => (
                                <li key={i}>{s}</li>
                              ))}
                            </ul>
                          </div>
                        </div>
                      </div>
                    ))}
                  </div>
                ) : (
                  <div className="card">
                    <div className="empty-state">
                      <FileText size={64} />
                      <h3>No sections analyzed</h3>
                      <p>Section analysis will appear here after the AI processes your report.</p>
                    </div>
                  </div>
                )}
              </div>
            )}

            {activeTab === 'issues' && (
              <div>
                {/* Filter */}
                <div style={{ marginBottom: '20px', display: 'flex', gap: '8px', flexWrap: 'wrap' }}>
                  {categories.map(cat => (
                    <button
                      key={cat}
                      className={`btn btn-sm ${!categoryFilter && cat === 'all' ? 'btn-primary' : 'btn-secondary'}`}
                      onClick={() => setCategoryFilter(cat === 'all' ? null : cat)}
                    >
                      {cat === 'all' ? 'All' : cat}
                      {cat !== 'all' && (
                        <span style={{
                          marginLeft: '4px',
                          fontSize: '0.75rem',
                          opacity: 0.7
                        }}>
                          ({issues.filter(i => i.category === cat).length})
                        </span>
                      )}
                    </button>
                  ))}
                </div>

                <div className="card">
                  {issues && issues.length > 0 ? (
                    <div className="table-container">
                      <table className="table">
                        <thead>
                          <tr>
                            <th>Severity</th>
                            <th>Category</th>
                            <th>Description</th>
                            <th>Location</th>
                            <th>Suggested Fix</th>
                          </tr>
                        </thead>
                        <tbody>
                          {filteredIssues(categoryFilter).map((issue) => (
                            <tr key={issue.id}>
                              <td>{getSeverityBadge(issue.severity)}</td>
                              <td>
                                <span style={{
                                  padding: '2px 8px',
                                  borderRadius: '4px',
                                  background: 'var(--gray-100)',
                                  fontSize: '0.8rem',
                                  textTransform: 'capitalize',
                                  fontWeight: 500
                                }}>
                                  {issue.category}
                                </span>
                              </td>
                              <td>{issue.description}</td>
                              <td>
                                {issue.location ? (
                                  <span style={{ color: 'var(--gray-600)' }}>{issue.location}</span>
                                ) : (
                                  <span style={{ color: 'var(--gray-400)' }}>-</span>
                                )}
                              </td>
                              <td>
                                <span style={{
                                  padding: '4px 8px',
                                  background: 'var(--primary-light)',
                                  borderRadius: '4px',
                                  fontSize: '0.85rem',
                                  color: 'var(--primary)'
                                }}>
                                  {issue.suggestion || 'No suggestion'}
                                </span>
                              </td>
                            </tr>
                          ))}
                        </tbody>
                      </table>
                    </div>
                  ) : (
                    <div className="empty-state">
                      <CheckCircle size={64} />
                      <h3>No issues found</h3>
                      <p>Great job! The AI didn't identify any significant issues.</p>
                    </div>
                  )}
                </div>
              </div>
            )}

            {activeTab === 'chat' && (
              <div className="card">
                <Chat reportId={id} />
              </div>
            )}
          </>
        ) : (
          <div className="card">
            <div className="empty-state">
              <FileText size={64} />
              <h3>Review not available</h3>
              <p>This report hasn't been analyzed yet.</p>
              <button className="btn btn-primary" onClick={analyzeReport} disabled={analyzing}>
                <Clock size={18} />
                {analyzing ? 'Analyzing...' : 'Start Analysis'}
              </button>
            </div>
          </div>
        )}
      </main>
    </div>
  );
}
