import { useEffect, useState } from 'react';
import { getRecommendations, runAgentStream } from '../api/jobs';
import { useAuth } from '../hooks/useAuth';

export default function HomePage() {
  const [jobs, setJobs] = useState([]);
  const [loading, setLoading] = useState(false);
  const [running, setRunning] = useState(false);
  const [currentStep, setCurrentStep] = useState('');
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

  const handleRunAgent = () => {
    setRunning(true);
    setCurrentStep('준비 중...');

    runAgentStream(
      (message) => setCurrentStep(message),
      () => {
        setRunning(false);
        setCurrentStep('');
        fetchRecommendations();
      },
      (error) => {
        setCurrentStep('');
        setRunning(false);
        alert(`오류가 발생했습니다: ${error}`);
      }
    );
  };

  useEffect(() => {
    fetchRecommendations();
  }, []);

  return (
    <div style={styles.page}>
      {running && (
        <div style={styles.overlay}>
          <div style={styles.overlayCard}>
            <div style={styles.spinnerWrap}>
              <div style={styles.spinner} />
            </div>
            <p style={styles.overlayTitle}>공고 분석 중</p>
            <p style={styles.overlayStep}>{currentStep}</p>
          </div>
        </div>
      )}

      <header style={styles.header}>
        <div style={styles.headerInner}>
          <div style={styles.headerLeft}>
            <div style={styles.logo}>JA</div>
            <span style={styles.headerTitle}>취업 AI 에이전트</span>
          </div>
          <div style={styles.headerRight}>
            <button
              style={{
                ...styles.runButton,
                opacity: running ? 0.7 : 1,
                cursor: running ? 'not-allowed' : 'pointer',
              }}
              onClick={handleRunAgent}
              disabled={running}
            >
              공고 수집 및 분석
            </button>
            <button style={styles.logoutButton} onClick={logout}>
              로그아웃
            </button>
          </div>
        </div>
      </header>

      <main style={styles.main}>
        <div style={styles.sectionHeader}>
          <h2 style={styles.sectionTitle}>추천 공고</h2>
          <span style={styles.sectionCount}>{jobs.length}개</span>
        </div>

        {loading ? (
          <div style={styles.emptyState}>
            <p style={styles.emptyText}>불러오는 중...</p>
          </div>
        ) : jobs.length === 0 ? (
          <div style={styles.emptyState}>
            <p style={styles.emptyText}>아직 추천 공고가 없습니다.</p>
            <p style={styles.emptySubText}>공고 수집 및 분석 버튼을 눌러주세요.</p>
          </div>
        ) : (
          <div style={styles.grid}>
            {jobs.map((job) => (
              <div key={job.id} style={styles.card}>
                <div style={styles.cardTop}>
                  <div style={styles.cardInfo}>
                    <p style={styles.company}>{job.company}</p>
                    <p style={styles.jobTitle}>{job.title}</p>
                  </div>
                  <div style={styles.scoreBadge}>
                    <span style={styles.scoreText}>{job.fit_score}%</span>
                  </div>
                </div>

                {job.summary && (
                  <p style={styles.summary}>{job.summary}</p>
                )}

                <div style={styles.cardBottom}>
                  {job.deadline ? (
                    <span style={styles.deadline}>마감 {job.deadline}</span>
                  ) : (
                    <span />
                  )}
                  <a
                    href={job.url}
                    target="_blank"
                    rel="noreferrer"
                    style={styles.link}
                  >
                    공고 보기
                  </a>
                </div>
              </div>
            ))}
          </div>
        )}
      </main>
    </div>
  );
}

const styles = {
  page: {
    minHeight: '100vh',
    backgroundColor: '#FAFAF7',
  },
  overlay: {
    position: 'fixed',
    top: 0,
    left: 0,
    right: 0,
    bottom: 0,
    backgroundColor: 'rgba(0,0,0,0.45)',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    zIndex: 999,
  },
  overlayCard: {
    backgroundColor: '#fff',
    borderRadius: '20px',
    padding: '48px 56px',
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    gap: '16px',
    boxShadow: '0 8px 40px rgba(0,0,0,0.12)',
    minWidth: '280px',
  },
  spinnerWrap: {
    marginBottom: '4px',
  },
  spinner: {
    width: '44px',
    height: '44px',
    border: '3px solid #EDE9FE',
    borderTop: '3px solid #C4B5FD',
    borderRadius: '50%',
    animation: 'spin 0.9s linear infinite',
  },
  overlayTitle: {
    fontSize: '17px',
    fontWeight: '700',
    color: '#2D2D2D',
  },
  overlayStep: {
    fontSize: '14px',
    color: '#888',
    textAlign: 'center',
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
  headerRight: {
    display: 'flex',
    alignItems: 'center',
    gap: '10px',
  },
  runButton: {
    padding: '8px 18px',
    backgroundColor: '#C4B5FD',
    color: '#fff',
    border: 'none',
    borderRadius: '8px',
    fontSize: '13px',
    fontWeight: '600',
  },
  logoutButton: {
    padding: '8px 18px',
    backgroundColor: 'transparent',
    color: '#888',
    border: '1px solid #E8E8E4',
    borderRadius: '8px',
    fontSize: '13px',
  },
  main: {
    maxWidth: '1100px',
    margin: '0 auto',
    padding: '32px 24px',
  },
  sectionHeader: {
    display: 'flex',
    alignItems: 'center',
    gap: '10px',
    marginBottom: '20px',
  },
  sectionTitle: {
    fontSize: '18px',
    fontWeight: '700',
    color: '#2D2D2D',
  },
  sectionCount: {
    fontSize: '13px',
    color: '#888',
    backgroundColor: '#F0F0EC',
    padding: '2px 10px',
    borderRadius: '20px',
  },
  emptyState: {
    textAlign: 'center',
    padding: '80px 0',
  },
  emptyText: {
    fontSize: '15px',
    color: '#555',
    marginBottom: '6px',
  },
  emptySubText: {
    fontSize: '13px',
    color: '#aaa',
  },
  grid: {
    display: 'grid',
    gridTemplateColumns: 'repeat(auto-fill, minmax(300px, 1fr))',
    gap: '16px',
  },
  card: {
    backgroundColor: '#fff',
    borderRadius: '14px',
    padding: '20px',
    border: '1px solid #EFEFEB',
    display: 'flex',
    flexDirection: 'column',
    gap: '12px',
  },
  cardTop: {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'flex-start',
    gap: '12px',
  },
  cardInfo: {
    flex: 1,
  },
  company: {
    fontSize: '13px',
    color: '#888',
    marginBottom: '4px',
  },
  jobTitle: {
    fontSize: '15px',
    fontWeight: '600',
    color: '#2D2D2D',
    lineHeight: '1.4',
  },
  scoreBadge: {
    backgroundColor: '#EDE9FE',
    borderRadius: '8px',
    padding: '6px 10px',
    flexShrink: 0,
  },
  scoreText: {
    fontSize: '14px',
    fontWeight: '700',
    color: '#7C3AED',
  },
  summary: {
    fontSize: '13px',
    color: '#666',
    lineHeight: '1.6',
  },
  cardBottom: {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginTop: 'auto',
  },
  deadline: {
    fontSize: '12px',
    color: '#F87171',
    backgroundColor: '#FFF5F5',
    padding: '4px 10px',
    borderRadius: '6px',
  },
  link: {
    fontSize: '13px',
    fontWeight: '600',
    color: '#7C3AED',
    padding: '6px 14px',
    backgroundColor: '#EDE9FE',
    borderRadius: '8px',
  },
};