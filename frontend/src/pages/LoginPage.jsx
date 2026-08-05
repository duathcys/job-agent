import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../hooks/useAuth';

export default function LoginPage() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const { login, loading, error } = useAuth();
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    const success = await login(email, password);
    if (success) navigate('/');
  };

  return (
    <div style={styles.container}>
      <div style={styles.card}>
        <div style={styles.logo}>JA</div>
        <h1 style={styles.title}>취업 AI 에이전트</h1>
        <p style={styles.subtitle}>나에게 맞는 공고를 AI가 찾아드립니다</p>

        {error && <div style={styles.errorBox}>{error}</div>}

        <form onSubmit={handleSubmit} style={styles.form}>
          <div style={styles.inputGroup}>
            <label style={styles.label}>이메일</label>
            <input
              style={styles.input}
              type="email"
              placeholder="example@email.com"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />
          </div>
          <div style={styles.inputGroup}>
            <label style={styles.label}>비밀번호</label>
            <input
              style={styles.input}
              type="password"
              placeholder="비밀번호를 입력해주세요"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
          </div>
          <button style={{...styles.button, opacity: loading ? 0.7 : 1}} type="submit" disabled={loading}>
            {loading ? '로그인 중...' : '로그인'}
          </button>
        </form>

        <p style={styles.link}>
          계정이 없으신가요? <Link to="/register" style={styles.linkText}>회원가입</Link>
        </p>
      </div>
    </div>
  );
}

const styles = {
  container: {
    display: 'flex',
    justifyContent: 'center',
    alignItems: 'center',
    minHeight: '100vh',
    backgroundColor: '#FAFAF7',
    padding: '16px',
  },
  card: {
    backgroundColor: '#fff',
    padding: '48px 40px',
    borderRadius: '20px',
    boxShadow: '0 4px 24px rgba(0,0,0,0.06)',
    width: '100%',
    maxWidth: '420px',
  },
  logo: {
    width: '48px',
    height: '48px',
    borderRadius: '14px',
    backgroundColor: '#C4B5FD',
    color: '#fff',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    fontWeight: '700',
    fontSize: '16px',
    marginBottom: '20px',
  },
  title: {
    fontSize: '22px',
    fontWeight: '700',
    color: '#2D2D2D',
    marginBottom: '6px',
  },
  subtitle: {
    fontSize: '14px',
    color: '#888',
    marginBottom: '32px',
  },
  errorBox: {
    backgroundColor: '#FFF0F0',
    color: '#E53E3E',
    padding: '12px 16px',
    borderRadius: '10px',
    fontSize: '13px',
    marginBottom: '16px',
  },
  form: {
    display: 'flex',
    flexDirection: 'column',
    gap: '16px',
  },
  inputGroup: {
    display: 'flex',
    flexDirection: 'column',
    gap: '6px',
  },
  label: {
    fontSize: '13px',
    fontWeight: '500',
    color: '#555',
  },
  input: {
    padding: '12px 16px',
    borderRadius: '10px',
    border: '1.5px solid #E8E8E4',
    fontSize: '14px',
    backgroundColor: '#FAFAF7',
    outline: 'none',
    transition: 'border-color 0.2s',
  },
  button: {
    padding: '14px',
    backgroundColor: '#C4B5FD',
    color: '#fff',
    border: 'none',
    borderRadius: '10px',
    fontSize: '15px',
    fontWeight: '600',
    marginTop: '8px',
    transition: 'background-color 0.2s',
  },
  link: {
    textAlign: 'center',
    marginTop: '24px',
    fontSize: '13px',
    color: '#888',
  },
  linkText: {
    color: '#C4B5FD',
    fontWeight: '600',
  },
};