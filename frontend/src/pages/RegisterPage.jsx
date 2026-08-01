import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { register } from '../api/auth';

export default function RegisterPage() {
  const [form, setForm] = useState({
    email: '',
    password: '',
    job: '백엔드',
    location: '서울',
    career: '신입',
    skills: '',
    interests: '',
  });
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    try {
      await register({
        ...form,
        skills: form.skills.split(',').map((s) => s.trim()),
        interests: form.interests.split(',').map((s) => s.trim()),
      });
      navigate('/login');
    } catch (e) {
      setError(e.response?.data?.detail || '회원가입 실패');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={styles.container}>
      <div style={styles.card}>
        <h1 style={styles.title}>회원가입</h1>

        {error && <p style={styles.error}>{error}</p>}

        <form onSubmit={handleSubmit} style={styles.form}>
          <input style={styles.input} name="email" type="email" placeholder="이메일" onChange={handleChange} required />
          <input style={styles.input} name="password" type="password" placeholder="비밀번호" onChange={handleChange} required />
          <input style={styles.input} name="job" placeholder="희망 직무 (예: 백엔드)" onChange={handleChange} defaultValue="백엔드" />
          <input style={styles.input} name="location" placeholder="지역 (예: 서울)" onChange={handleChange} defaultValue="서울" />
          <input style={styles.input} name="career" placeholder="경력 (예: 신입)" onChange={handleChange} defaultValue="신입" />
          <input style={styles.input} name="skills" placeholder="기술스택 (쉼표로 구분: Java, Spring, MySQL)" onChange={handleChange} />
          <input style={styles.input} name="interests" placeholder="관심 기업 (쉼표로 구분: 네이버, 카카오)" onChange={handleChange} />
          <button style={styles.button} type="submit" disabled={loading}>
            {loading ? '가입 중...' : '회원가입'}
          </button>
        </form>

        <p style={styles.link}>
          이미 계정이 있으신가요? <Link to="/login">로그인</Link>
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
    backgroundColor: '#f5f5f5',
  },
  card: {
    backgroundColor: '#fff',
    padding: '40px',
    borderRadius: '12px',
    boxShadow: '0 2px 10px rgba(0,0,0,0.1)',
    width: '400px',
  },
  title: { textAlign: 'center', marginBottom: '24px', color: '#333' },
  form: { display: 'flex', flexDirection: 'column', gap: '12px' },
  input: {
    padding: '12px',
    borderRadius: '8px',
    border: '1px solid #ddd',
    fontSize: '14px',
  },
  button: {
    padding: '12px',
    backgroundColor: '#4F46E5',
    color: '#fff',
    border: 'none',
    borderRadius: '8px',
    fontSize: '16px',
    cursor: 'pointer',
  },
  error: { color: 'red', fontSize: '14px', textAlign: 'center' },
  link: { textAlign: 'center', marginTop: '16px', fontSize: '14px' },
};