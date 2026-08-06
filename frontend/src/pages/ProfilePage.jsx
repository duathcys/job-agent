import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { getMe, updateMe } from '../api/auth';
import { uploadResume } from '../api/resume';

export default function ProfilePage() {
  const [form, setForm] = useState(null);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [success, setSuccess] = useState(false);
  const [error, setError] = useState(null);
  const navigate = useNavigate();
  const [resumeLoading, setResumeLoading] = useState(false);
  const [resumeResult, setResumeResult] = useState(null);

  useEffect(() => {
    getMe()
      .then((res) => {
        setForm({
          ...res.data,
          skills: res.data.skills.join(', '),
          interests: (res.data.interests || []).join(', '),
        });
      })
      .catch(() => navigate('/login'))
      .finally(() => setLoading(false));
  }, []);

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleResumeUpload = async (e) => {
    const file = e.target.files[0];
    if (!file) return;
    setResumeLoading(true);
    setResumeResult(null);
    try {
        const res = await uploadResume(file, false);
        setResumeResult(res.data.result);
    } catch (e) {
        setError('이력서 분석에 실패했습니다.');
    } finally {
        setResumeLoading(false);
    }
    };

  const handleApplyResume = async () => {
    if (!resumeResult) return;
    setSaving(true);
    try {
        await updateMe({
        job: resumeResult.job,
        career: resumeResult.career,
        skills: resumeResult.skills,
        });
        setForm({
        ...form,
        job: resumeResult.job,
        career: resumeResult.career,
        skills: resumeResult.skills.join(', '),
        });
        setSuccess(true);
        setResumeResult(null);
        setTimeout(() => setSuccess(false), 3000);
    } catch (e) {
        setError('프로필 적용에 실패했습니다.');
    } finally {
        setSaving(false);
    }
    };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setSaving(true);
    setError(null);
    setSuccess(false);
    try {
      await updateMe({
        job: form.job,
        location: form.location,
        career: form.career,
        skills: form.skills.split(',').map((s) => s.trim()).filter(Boolean),
        interests: form.interests.split(',').map((s) => s.trim()).filter(Boolean),
      });
      setSuccess(true);
      setTimeout(() => setSuccess(false), 3000);
    } catch (e) {
      setError('저장에 실패했습니다. 다시 시도해주세요.');
    } finally {
      setSaving(false);
    }
  };

  if (loading || !form) {
    return (
      <div style={styles.page}>
        <div style={styles.loading}>불러오는 중...</div>
      </div>
    );
  }

  return (
    <div style={styles.page}>
      <header style={styles.header}>
        <div style={styles.headerInner}>
          <div style={styles.headerLeft}>
            <div style={styles.logo}>JA</div>
            <span style={styles.headerTitle}>취업 AI 에이전트</span>
          </div>
          <button style={styles.backButton} onClick={() => navigate('/')}>
            홈으로
          </button>
        </div>
      </header>

      <main style={styles.main}>
        <div style={styles.card}>
          <h1 style={styles.title}>내 정보</h1>
          <p style={styles.subtitle}>{form.email}</p>
          <div style={styles.resumeSection}>
            <p style={styles.resumeTitle}>이력서로 자동 분석</p>
            <label style={styles.uploadLabel}>
                <input
                type="file"
                accept=".pdf"
                onChange={handleResumeUpload}
                style={{ display: 'none' }}
                />
                {resumeLoading ? '분석 중...' : 'PDF 이력서 업로드'}
            </label>

            {resumeResult && (
                <div style={styles.resumeResult}>
                <p style={styles.resumeResultTitle}>분석 결과</p>
                <p style={styles.resumeItem}><b>직무:</b> {resumeResult.job}</p>
                <p style={styles.resumeItem}><b>경력:</b> {resumeResult.career}</p>
                <p style={styles.resumeItem}><b>기술:</b> {resumeResult.skills?.join(', ')}</p>
                <p style={styles.resumeItem}><b>요약:</b> {resumeResult.summary}</p>
                {resumeResult.missing_skills?.length > 0 && (
                    <p style={styles.resumeItem}><b>부족한 기술:</b> {resumeResult.missing_skills.join(', ')}</p>
                )}
                <button style={styles.applyButton} onClick={handleApplyResume}>
                    프로필에 적용
                </button>
                </div>
            )}
            </div>

          {error && <div style={styles.errorBox}>{error}</div>}
          {success && <div style={styles.successBox}>저장되었습니다!</div>}

          <form onSubmit={handleSubmit} style={styles.form}>
            {[
              { name: 'job', label: '희망 직무', placeholder: '예: 백엔드' },
              { name: 'location', label: '희망 지역', placeholder: '예: 서울' },
              { name: 'career', label: '경력', placeholder: '예: 신입' },
              { name: 'skills', label: '기술스택', placeholder: '쉼표로 구분: Java, Spring, MySQL' },
              { name: 'interests', label: '관심 기업', placeholder: '쉼표로 구분: 네이버, 카카오' },
            ].map(({ name, label, placeholder }) => (
              <div key={name} style={styles.inputGroup}>
                <label style={styles.label}>{label}</label>
                <input
                  style={styles.input}
                  name={name}
                  placeholder={placeholder}
                  value={form[name] || ''}
                  onChange={handleChange}
                />
              </div>
            ))}

            <div style={styles.buttonRow}>
              <button
                style={styles.cancelButton}
                type="button"
                onClick={() => navigate('/')}
              >
                취소
              </button>
              <button
                style={{ ...styles.saveButton, opacity: saving ? 0.7 : 1 }}
                type="submit"
                disabled={saving}
              >
                {saving ? '저장 중...' : '저장'}
              </button>
            </div>
          </form>
        </div>
      </main>
    </div>
  );
}

const styles = {
  page: {
    minHeight: '100vh',
    backgroundColor: '#FAFAF7',
  },
  loading: {
    textAlign: 'center',
    padding: '80px',
    color: '#888',
  },
  header: {
    backgroundColor: '#fff',
    borderBottom: '1px solid #EFEFEB',
    position: 'sticky',
    top: 0,
    zIndex: 100,
  },
  headerInner: {
    maxWidth: '1100px',
    margin: '0 auto',
    padding: '0 24px',
    height: '64px',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'space-between',
  },
  headerLeft: {
    display: 'flex',
    alignItems: 'center',
    gap: '12px',
  },
  logo: {
    width: '36px',
    height: '36px',
    borderRadius: '10px',
    backgroundColor: '#C4B5FD',
    color: '#fff',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    fontWeight: '700',
    fontSize: '13px',
  },
  headerTitle: {
    fontSize: '15px',
    fontWeight: '600',
    color: '#2D2D2D',
  },
  backButton: {
    padding: '8px 18px',
    backgroundColor: 'transparent',
    color: '#888',
    border: '1px solid #E8E8E4',
    borderRadius: '8px',
    fontSize: '13px',
    cursor: 'pointer',
  },
  main: {
    maxWidth: '560px',
    margin: '0 auto',
    padding: '40px 24px',
  },
  card: {
    backgroundColor: '#fff',
    borderRadius: '20px',
    padding: '40px',
    border: '1px solid #EFEFEB',
  },
  title: {
    fontSize: '22px',
    fontWeight: '700',
    color: '#2D2D2D',
    marginBottom: '4px',
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
  successBox: {
    backgroundColor: '#F0FFF4',
    color: '#38A169',
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
  },
  buttonRow: {
    display: 'flex',
    gap: '10px',
    marginTop: '8px',
  },
  cancelButton: {
    flex: 1,
    padding: '14px',
    backgroundColor: 'transparent',
    color: '#888',
    border: '1px solid #E8E8E4',
    borderRadius: '10px',
    fontSize: '15px',
    fontWeight: '600',
    cursor: 'pointer',
  },
  saveButton: {
    flex: 2,
    padding: '14px',
    backgroundColor: '#C4B5FD',
    color: '#fff',
    border: 'none',
    borderRadius: '10px',
    fontSize: '15px',
    fontWeight: '600',
    cursor: 'pointer',
  },
  resumeSection: {
    backgroundColor: '#F5F3FF',
    borderRadius: '12px',
    padding: '20px',
    marginBottom: '24px',
    },
  resumeTitle: {
    fontSize: '13px',
    fontWeight: '600',
    color: '#7C3AED',
    marginBottom: '12px',
    },
  uploadLabel: {
    display: 'inline-block',
    padding: '10px 20px',
    backgroundColor: '#C4B5FD',
    color: '#fff',
    borderRadius: '8px',
    fontSize: '13px',
    fontWeight: '600',
    cursor: 'pointer',
    },
  resumeResult: {
    marginTop: '16px',
    padding: '16px',
    backgroundColor: '#fff',
    borderRadius: '10px',
    border: '1px solid #E8E8E4',
    display: 'flex',
    flexDirection: 'column',
    gap: '6px',
    },
  resumeResultTitle: {
    fontSize: '13px',
    fontWeight: '600',
    color: '#2D2D2D',
    marginBottom: '4px',
    },
  resumeItem: {
    fontSize: '13px',
    color: '#555',
    },
  applyButton: {
    marginTop: '8px',
    padding: '10px',
    backgroundColor: '#7C3AED',
    color: '#fff',
    border: 'none',
    borderRadius: '8px',
    fontSize: '13px',
    fontWeight: '600',
    cursor: 'pointer',
    },
};