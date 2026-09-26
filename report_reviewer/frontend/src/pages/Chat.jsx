import { useState, useRef, useEffect } from 'react';
import { useChat } from '../hooks/useReports';
import { Send, ShieldAlert, Bot, RefreshCw, CheckCircle } from 'lucide-react';

export function Chat({ reportId }) {
  const {
    messages,
    sending,
    error,
    suggestedQuestions,
    context,
    demoMode,
    sendMessage,
    clearChat,
    loadSuggestedQuestions,
  } = useChat(reportId);

  const [inputValue, setInputValue] = useState('');
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSend = async () => {
    if (!inputValue.trim() || sending) return;

    const userMessage = inputValue.trim();
    setInputValue('');
    await sendMessage(userMessage);
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  const handleSuggestedQuestion = (question) => {
    setInputValue(question);
  };

  return (
    <div className="chat-container">
      {/* Header */}
      <div style={{
        padding: '16px 20px',
        borderBottom: '1px solid var(--gray-200)',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between',
        background: 'var(--gray-50)'
      }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
          <div style={{
            width: '40px',
            height: '40px',
            borderRadius: '50%',
            background: 'var(--primary)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            color: 'white'
          }}>
            <Bot size={20} />
          </div>
          <div>
            <h4 style={{ margin: 0, fontSize: '1rem' }}>AI Chat Assistant</h4>
            <p style={{ margin: 0, fontSize: '0.8rem', color: 'var(--gray-600)' }}>
              Ask questions about your report
            </p>
          </div>
        </div>
        <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
          {demoMode && (
            <div style={{
              padding: '4px 10px',
              background: '#fff3cd',
              borderRadius: '9999px',
              fontSize: '0.75rem',
              color: '#856404',
              display: 'flex',
              alignItems: 'center',
              gap: '4px'
            }}>
              <ShieldAlert size={12} />
              Demo Mode
            </div>
          )}
          {context?.has_review && (
            <span style={{
              padding: '4px 10px',
              background: '#d4edda',
              borderRadius: '9999px',
              fontSize: '0.75rem',
              color: '#155724',
              display: 'flex',
              alignItems: 'center',
              gap: '4px'
            }}>
              <CheckCircle size={12} />
              Review Available
            </span>
          )}
        </div>
      </div>

      {/* Messages */}
      <div className="chat-messages">
        {messages.length === 0 ? (
          <div className="chat-empty-state">
            <Bot size={48} className="chat-empty-icon" />
            <p className="chat-empty-title">
              Ask me anything about your report
            </p>
            <p className="chat-empty-description">
              I can help you improve sections, explain scores, and provide writing suggestions.
            </p>
          </div>
        ) : (
          messages.map((msg, index) => (
            <div
              key={index}
              className={`chat-message ${msg.role}`}
            >
              {msg.role === 'user' && (
                <div className="chat-message-avatar">
                  <span>You</span>
                </div>
              )}
              {msg.role === 'assistant' && (
                <div className="chat-message-avatar chat-message-avatar-ai">
                  <span>AI</span>
                </div>
              )}
              <div className="chat-message-content">{msg.content}</div>
            </div>
          ))
        )}
        <div ref={messagesEndRef} />
      </div>

      {error && (
        <div className="alert alert-error" style={{ margin: '0 20px 12px' }}>
          {error}
        </div>
      )}

      {/* Suggested Questions */}
      {suggestedQuestions.length > 0 && messages.length < 3 && (
        <div className="suggested-questions">
          {suggestedQuestions.map((q, index) => (
            <button
              key={index}
              className="suggested-question"
              onClick={() => handleSuggestedQuestion(q)}
            >
              {q}
            </button>
          ))}
        </div>
      )}

      {/* Input Area */}
      <div className="chat-input-container">
        <input
          type="text"
          className="chat-message-input"
          placeholder="Ask a question about your report..."
          value={inputValue}
          onChange={(e) => setInputValue(e.target.value)}
          onKeyDown={handleKeyDown}
          disabled={sending}
        />
        <button
          className="chat-send-btn"
          onClick={handleSend}
          disabled={!inputValue.trim() || sending}
        >
          {sending ? (
            <RefreshCw size={18} style={{ animation: 'spin 1s linear infinite' }} />
          ) : (
            <Send size={18} />
          )}
        </button>
      </div>
    </div>
  );
}
