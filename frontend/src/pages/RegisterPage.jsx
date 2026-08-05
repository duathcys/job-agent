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
        skills: form.skills.split(',').map((s) => s.trim()).filter(Boolean),
        interests: form.interests.split(',').map((s) => s.trim()).filter(Boolean),
      });
      navigate('/login');
    } catch (e) {
      setError(e.response?.data?.detail || '회원가입에 실패했습니다. 다시 시도해주세요.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={styles.container}>
      <div style={styles.card}>
        <div style={styles.logo}>JA</div>
        <h1 style={styles.title}>회원가입</h1>
        <p style={styles.subtitle}>취업 정보를 입력해주세요</p>

        {error && <div style={styles.errorBox}>{error}</div>}

        <form onSubmit={handleSubmit} style={styles.form}>
          {[
            { name: 'email', label: '이메일', type: 'email', placeholder: 'example@email.com' },
            { name: 'password', label: '비밀번호', type: 'password', placeholder: '비밀번호를 입력해주세요' },
            { name: 'job', label: '희망 직무', type: 'text', placeholder: '예: 백엔드' },
            { name: 'location', label: '희망 지역', type: 'text', placeholder: '예: 서울' },
            { name: 'career', label: '경력', type: 'text', placeholder: '예: 신입' },
            { name: 'skills', label: '기술스택', type: 'text', placeholder: '쉼표로 구분: Java, Spring, MySQL' },
            { name: 'interests', label: '관심 기업', type: 'text', placeholder: '쉼표로 구분: 네이버, 카카오' },
          ].map(({ name, label, type, placeholder }) => (
            <div key={name} style={styles.inputGroup}>
              <label style={styles.label}>{label}</label>
              <input
                style={styles.input}
                name={name}
                type={type}
                placeholder={placeholder}
                defaultValue={form[name]}
                onChange={handleChange}
                required={['email', 'password', 'job', 'location', 'career'].includes(name)}
              />
            </div>
          ))}

          <button style={{...styles.button, opacity: loading ? 0.7 : 1}} type="submit" disabled={loading}>
            {loading ? '가입 중...' : '시작하기'}
          </button>
        </form>

        <p style={styles.link}>
          이미 계정이 있으신가요? <Link to="/login" style={styles.linkText}>로그인</Link>
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
    padding: '24px 16px',
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
    gap: '14px',
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