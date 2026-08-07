import { useEffect, useRef, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import client from '../api/client';

const SUGGESTIONS = [
  "백엔드 공고 찾아줘",
  "내 스킬에 맞는 공고 추천해줘",
  "네이버 공고 있어?",
  "Docker 없어도 되는 공고 있어?",
  "적합도 높은 공고 보여줘",
];

export default function ChatPage() {
  const [messages, setMessages] = useState([
    {
      role: 'assistant',
      content: '안녕하세요! 취업 AI 에이전트입니다. 채용공고 검색, 적합도 분석, 공고 추천 등 무엇이든 물어보세요!',
    },
  ]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const bottomRef = useRef(null);
  const navigate = useNavigate();

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const sendMessage = async (text) => {
    const message = text || input.trim();
    if (!message || loading) return;

    setMessages((prev) => [...prev, { role: 'user', content: message }]);
    setInput('');
    setLoading(true);

    try {
      const res = await client.post('/chat/', { message });
      setMessages((prev) => [
        ...prev,
        { role: 'assistant', content: res.data.response },
      ]);
    } catch (e) {
      setMessages((prev) => [
        ...prev,
        { role: 'assistant', content: '오류가 발생했습니다. 다시 시도해주세요.' },
      ]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={styles.page}>
      <header style={styles.header}>
        <div style={styles.headerInner}>
          <div style={styles.headerLeft}>
            <div style={styles.logo}>JA</div>
            <span style={styles.headerTitle}>AI 채팅</span>
          </div>
          <button style={styles.backButton} onClick={() => navigate('/')}>
            홈으로
          </button>
        </div>
      </header>

      <main style={styles.main}>
        <div style={styles.chatContainer}>
          <div style={styles.messages}>
            {messages.map((msg, i) => (
              <div
                key={i}
                style={{
                  ...styles.message,
                  ...(msg.role === 'user' ? styles.userMessage : styles.assistantMessage),
                }}
              >
                {msg.role === 'assistant' && (
                  <div style={styles.avatar}>JA</div>
                )}
                <div
                  style={{
                    ...styles.bubble,
                    ...(msg.role === 'user' ? styles.userBubble : styles.assistantBubble),
                  }}
                >
                  <p style={styles.bubbleText}>{msg.content}</p>
                </div>
              </div>
            ))}
            {loading && (
              <div style={styles.message}>
                <div style={styles.avatar}>JA</div>
                <div style={styles.assistantBubble}>
                  <p style={styles.bubbleText}>분석 중...</p>
                </div>
              </div>
            )}
            <div ref={bottomRef} />
          </div>

          {messages.length === 1 && (
            <div style={styles.suggestions}>
              {SUGGESTIONS.map((s) => (
                <button
                  key={s}
                  style={styles.suggestionButton}
                  onClick={() => sendMessage(s)}
                >
                  {s}
                </button>
              ))}
            </div>
          )}

          <div style={styles.inputRow}>
            <input
              style={styles.input}
              placeholder="메시지를 입력하세요..."
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={(e) => e.key === 'Enter' && sendMessage()}
              disabled={loading}
            />
            <button
              style={{ ...styles.sendButton, opacity: loading ? 0.7 : 1 }}
              onClick={() => sendMessage()}
              disabled={loading}
            >
              전송
            </button>
          </div>
        </div>
      </main>
    </div>
  );
}

const styles = {
  page: { minHeight: '100vh', backgroundColor: '#FAFAF7', display: 'flex', flexDirection: 'column' },
  header: { backgroundColor: '#fff', borderBottom: '1px solid #EFEFEB', position: 'sticky', top: 0, zIndex: 100 },
  headerInner: { maxWidth: '1100px', margin: '0 auto', padding: '0 24px', height: '64px', display: 'flex', alignItems: 'center', justifyContent: 'space-between' },
  headerLeft: { display: 'flex', alignItems: 'center', gap: '12px' },
  logo: { width: '36px', height: '36px', borderRadius: '10px', backgroundColor: '#C4B5FD', color: '#fff', display: 'flex', alignItems: 'center', justifyContent: 'center', fontWeight: '700', fontSize: '13px' },
  headerTitle: { fontSize: '15px', fontWeight: '600', color: '#2D2D2D' },
  backButton: { padding: '8px 18px', backgroundColor: 'transparent', color: '#888', border: '1px solid #E8E8E4', borderRadius: '8px', fontSize: '13px', cursor: 'pointer' },
  main: { flex: 1, display: 'flex', justifyContent: 'center', padding: '24px' },
  chatContainer: { width: '100%', maxWidth: '760px', display: 'flex', flexDirection: 'column', gap: '16px' },
  messages: { display: 'flex', flexDirection: 'column', gap: '16px', minHeight: '400px' },
  message: { display: 'flex', alignItems: 'flex-start', gap: '10px' },
  userMessage: { flexDirection: 'row-reverse' },
  assistantMessage: { flexDirection: 'row' },
  avatar: { width: '32px', height: '32px', borderRadius: '10px', backgroundColor: '#C4B5FD', color: '#fff', display: 'flex', alignItems: 'center', justifyContent: 'center', fontWeight: '700', fontSize: '11px', flexShrink: 0 },
  bubble: { maxWidth: '70%', padding: '12px 16px', borderRadius: '14px' },
  userBubble: { backgroundColor: '#C4B5FD', color: '#fff', borderTopRightRadius: '4px' },
  assistantBubble: { backgroundColor: '#fff', border: '1px solid #EFEFEB', borderTopLeftRadius: '4px' },
  bubbleText: { fontSize: '14px', lineHeight: '1.6', whiteSpace: 'pre-wrap' },
  suggestions: { display: 'flex', flexWrap: 'wrap', gap: '8px' },
  suggestionButton: { padding: '8px 16px', backgroundColor: '#fff', color: '#7C3AED', border: '1px solid #C4B5FD', borderRadius: '20px', fontSize: '13px', cursor: 'pointer' },
  inputRow: { display: 'flex', gap: '10px', position: 'sticky', bottom: '24px' },
  input: { flex: 1, padding: '14px 18px', borderRadius: '12px', border: '1.5px solid #E8E8E4', fontSize: '14px', backgroundColor: '#fff', outline: 'none' },
  sendButton: { padding: '14px 24px', backgroundColor: '#C4B5FD', color: '#fff', border: 'none', borderRadius: '12px', fontSize: '14px', fontWeight: '600', cursor: 'pointer' },
};