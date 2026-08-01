import { useEffect, useState } from 'react';
import { getRecommendations, runAgent } from '../api/jobs';
import { useAuth } from '../hooks/useAuth';

export default function HomePage() {
  const [jobs, setJobs] = useState([]);
  const [loading, setLoading] = useState(false);
  const [running, setRunning] = useState(false);
  const { logout } = useAuth();

  const fetchRecommendations = async () => {
    setLoading(true);
    try {
      const res = await getRecommendations();
      setJobs(res.data);
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  const handleRunAgent = async () => {
    setRunning(true);
    try {
      await runAgent();
      alert('에이전트 실행 완료! 잠시 후 새로고침해주세요.');
    } catch (e) {
      alert('에이전트 실행 실패');
    } finally {
      setRunning(false);
    }
  };

  useEffect(() => {
    fetchRecommendations();
  }, []);

  return (
    <div style={styles.container}>
      <div style={styles.header}>
        <h1 style={styles.title}>🎯 취업 AI 에이전트</h1>
        <div style={styles.headerButtons}>
          <button style={styles.runButton} onClick={handleRunAgent} disabled={running}>
            {running ? '실행 중...' : '🔄 공고 수집 & 분석'}
          </button>
          <button style={styles.logoutButton} onClick={logout}>
            로그아웃
          </button>
        </div>
      </div>

      <h2 style={styles.sectionTitle}>📋 추천 공고</h2>

      {loading ? (
        <p style={styles.loading}>불러오는 중...</p>
      ) : jobs.length === 0 ? (
        <p style={styles.empty}>추천 공고가 없습니다. 공고 수집 & 분석을 실행해주세요.</p>
      ) : (
        <div style={styles.grid}>
          {jobs.map((job) => (
            <div key={job.id} style={styles.card}>
              <div style={styles.scoreBar}>
                <span style={styles.score}>적합도 {job.fit_score}%</span>
              </div>
              <h3 style={styles.company}>{job.company}</h3>
              <p style={styles.jobTitle}>{job.title}</p>
              <p style={styles.summary}>{job.summary}</p>
              {job.deadline && (
                <p style={styles.deadline}>⏰ 마감일: {job.deadline}</p>
              )}
              <a
              
                href={job.url}
                target="_blank"
                rel="noreferrer"
                style={styles.link}
                >
                공고 보러가기 →
              </a>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

const styles = {
  container: { maxWidth: '1100px', margin: '0 auto', padding: '32px 16px' },
  header: {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: '32px',
  },
  title: { color: '#333', margin: 0 },
  headerButtons: { display: 'flex', gap: '12px' },
  runButton: {
    padding: '10px 20px',
    backgroundColor: '#4F46E5',
    color: '#fff',
    border: 'none',
    borderRadius: '8px',
    cursor: 'pointer',
    fontSize: '14px',
  },
  logoutButton: {
    padding: '10px 20px',
    backgroundColor: '#fff',
    color: '#666',
    border: '1px solid #ddd',
    borderRadius: '8px',
    cursor: 'pointer',
    fontSize: '14px',
  },
  sectionTitle: { color: '#333', marginBottom: '16px' },
  loading: { color: '#888', textAlign: 'center', marginTop: '40px' },
  empty: { color: '#888', textAlign: 'center', marginTop: '40px' },
  grid: {
    display: 'grid',
    gridTemplateColumns: 'repeat(auto-fill, minmax(320px, 1fr))',
    gap: '20px',
  },
  card: {
    backgroundColor: '#fff',
    borderRadius: '12px',
    padding: '24px',
    boxShadow: '0 2px 8px rgba(0,0,0,0.08)',
    display: 'flex',
    flexDirection: 'column',
    gap: '8px',
  },
  scoreBar: {
    display: 'flex',
    justifyContent: 'flex-end',
  },
  score: {
    backgroundColor: '#EEF2FF',
    color: '#4F46E5',
    padding: '4px 10px',
    borderRadius: '20px',
    fontSize: '13px',
    fontWeight: 'bold',
  },
  company: { margin: 0, color: '#333', fontSize: '16px' },
  jobTitle: { margin: 0, color: '#555', fontSize: '14px' },
  summary: { margin: 0, color: '#777', fontSize: '13px', lineHeight: '1.5' },
  deadline: { margin: 0, color: '#e57373', fontSize: '13px' },
  link: {
    color: '#4F46E5',
    fontSize: '14px',
    textDecoration: 'none',
    marginTop: '4px',
  },
};