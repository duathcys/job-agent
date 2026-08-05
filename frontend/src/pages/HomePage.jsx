import { useEffect, useState } from 'react';
import { getRecommendations, runAgentStream } from '../api/jobs';
import { useAuth } from '../hooks/useAuth';

export default function HomePage() {
  const [jobs, setJobs] = useState([]);
  const [loading, setLoading] = useState(false);
  const [running, setRunning] = useState(false);
  const [logs, setLogs] = useState([]);
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
    setLogs([]);

    runAgentStream(
      (message) => setLogs((prev) => [...prev, message]),
      () => {
        setRunning(false);
        fetchRecommendations();
      },
      (error) => {
        setLogs((prev) => [...prev, `오류: ${error}`]);
        setRunning(false);
      }
    );
  };

  useEffect(() => {
    fetchRecommendations();
  }, []);

  return (
    <div style={styles.page}>
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
              {running ? '분석 중...' : '공고 수집 및 분석'}
            </button>
            <button style={styles.logoutButton} onClick={logout}>
              로그아웃
            </button>
          </div>
        </div>
      </header>

      <main style={styles.main}>
        {(running || logs.length > 0) && (
          <div style={styles.progressCard}>
            <p style={styles.progressTitle}>진행 상황</p>
            <div style={styles.logList}>
              {logs.map((log, i) => (
                <div key={i} style={styles.logItem}>
                  <span style={styles.logDot} />
                  <span>{log}</span>
                </div>
              ))}
              {running && (
                <div style={styles.logItem}>
                  <span style={{...styles.logDot, backgroundColor: '#FCD34D'}} />
                  <span style={{color: '#888'}}>처리 중...</span>
                </div>
              )}
            </div>
          </div>
        )}

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
                  <div>
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
                  {job.deadline && (
                    <span style={styles.deadline}>마감 {job.deadline}</span>
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
  progressCard: {
    backgroundColor: '#fff',
    borderRadius: '14px',
    padding: '20px 24px',
    marginBottom: '28px',
    border: '1px solid #EFEFEB',
  },
  progressTitle: {
    fontSize: '13px',
    fontWeight: '600',
    color: '#888',
    marginBottom: '12px',
    textTransform: 'uppercase',
    letterSpacing: '0.05em',
  },
  logList: {
    display: 'flex',
    flexDirection: 'column',
    gap: '8px',
  },
  logItem: {
    display: 'flex',
    alignItems: 'center',
    gap: '10px',
    fontSize: '14px',
    color: '#2D2D2D',
  },
  logDot: {
    width: '8px',
    height: '8px',
    borderRadius: '50%',
    backgroundColor: '#A7F3D0',
    flexShrink: 0,
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
    transition: 'box-shadow 0.2s',
  },
  cardTop: {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'flex-start',
    gap: '12px',
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