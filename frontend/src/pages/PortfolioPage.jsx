import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import client from '../api/client';

export default function PortfolioPage() {
  const [file, setFile] = useState(null);
  const [output, setOutput] = useState('html');
  const [loading, setLoading] = useState(false);
  const [htmlResult, setHtmlResult] = useState(null);
  const navigate = useNavigate();

  const handleGenerate = async () => {
    setLoading(true);
    setHtmlResult(null);

    try {
      const formData = new FormData();
      if (file) formData.append('file', file);

      const res = await client.post(
        `/portfolio/generate?output=${output}`,
        formData,
        {
          headers: { 'Content-Type': 'multipart/form-data' },
          responseType: output === 'pdf' ? 'blob' : 'text',
        }
      );

      if (output === 'pdf') {
        const url = URL.createObjectURL(new Blob([res.data], { type: 'application/pdf' }));
        const a = document.createElement('a');
        a.href = url;
        a.download = 'portfolio.pdf';
        a.click();
      } else {
        setHtmlResult(res.data);
      }
    } catch (e) {
      alert('포트폴리오 생성에 실패했습니다.');
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
            <span style={styles.headerTitle}>취업 AI 에이전트</span>
          </div>
          <button style={styles.backButton} onClick={() => navigate('/')}>
            홈으로
          </button>
        </div>
      </header>

      <main style={styles.main}>
        {htmlResult ? (
          <div>
            <div style={styles.resultHeader}>
              <h2 style={styles.sectionTitle}>포트폴리오 미리보기</h2>
              <div style={styles.resultButtons}>
                <button
                  style={styles.resetButton}
                  onClick={() => setHtmlResult(null)}
                >
                  다시 만들기
                </button>
                <button
                  style={styles.downloadButton}
                  onClick={() => {
                    const blob = new Blob([htmlResult], { type: 'text/html' });
                    const url = URL.createObjectURL(blob);
                    const a = document.createElement('a');
                    a.href = url;
                    a.download = 'portfolio.html';
                    a.click();
                  }}
                >
                  HTML 다운로드
                </button>
              </div>
            </div>
            <iframe
              srcDoc={htmlResult}
              style={styles.preview}
              title="포트폴리오 미리보기"
            />
          </div>
        ) : (
          <div style={styles.card}>
            <h1 style={styles.title}>포트폴리오 생성</h1>
            <p style={styles.subtitle}>
              PDF 이력서를 업로드하면 AI가 포트폴리오를 자동으로 만들어드립니다.
            </p>

            <div style={styles.section}>
              <p style={styles.label}>이력서 업로드 (선택)</p>
              <label style={styles.uploadLabel}>
                <input
                  type="file"
                  accept=".pdf"
                  onChange={(e) => setFile(e.target.files[0])}
                  style={{ display: 'none' }}
                />
                {file ? file.name : 'PDF 파일 선택'}
              </label>
              {file && (
                <button
                  style={styles.removeFile}
                  onClick={() => setFile(null)}
                >
                  제거
                </button>
              )}
              <p style={styles.hint}>
                업로드하지 않으면 프로필 정보로 생성됩니다.
              </p>
            </div>

            <div style={styles.section}>
              <p style={styles.label}>출력 형식</p>
              <div style={styles.outputButtons}>
                <button
                  style={{
                    ...styles.outputButton,
                    ...(output === 'html' ? styles.outputButtonActive : {}),
                  }}
                  onClick={() => setOutput('html')}
                >
                  HTML
                </button>
                <button
                  style={{
                    ...styles.outputButton,
                    ...(output === 'pdf' ? styles.outputButtonActive : {}),
                  }}
                  onClick={() => setOutput('pdf')}
                >
                  PDF
                </button>
              </div>
            </div>

            <button
              style={{ ...styles.generateButton, opacity: loading ? 0.7 : 1 }}
              onClick={handleGenerate}
              disabled={loading}
            >
              {loading ? 'AI가 생성 중...' : '포트폴리오 생성'}
            </button>
          </div>
        )}
      </main>
    </div>
  );
}

const styles = {
  page: { minHeight: '100vh', backgroundColor: '#FAFAF7' },
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
  headerLeft: { display: 'flex', alignItems: 'center', gap: '12px' },
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
  headerTitle: { fontSize: '15px', fontWeight: '600', color: '#2D2D2D' },
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
    maxWidth: '680px',
    margin: '0 auto',
    padding: '40px 24px',
  },
  card: {
    backgroundColor: '#fff',
    borderRadius: '20px',
    padding: '40px',
    border: '1px solid #EFEFEB',
  },
  title: { fontSize: '22px', fontWeight: '700', color: '#2D2D2D', marginBottom: '6px' },
  subtitle: { fontSize: '14px', color: '#888', marginBottom: '32px' },
  section: { marginBottom: '24px' },
  label: { fontSize: '13px', fontWeight: '500', color: '#555', marginBottom: '10px' },
  uploadLabel: {
    display: 'inline-block',
    padding: '10px 20px',
    backgroundColor: '#F5F3FF',
    color: '#7C3AED',
    borderRadius: '8px',
    fontSize: '13px',
    fontWeight: '600',
    cursor: 'pointer',
    border: '1px solid #C4B5FD',
  },
  removeFile: {
    marginLeft: '10px',
    padding: '8px 14px',
    backgroundColor: 'transparent',
    color: '#888',
    border: '1px solid #E8E8E4',
    borderRadius: '8px',
    fontSize: '12px',
    cursor: 'pointer',
  },
  hint: { fontSize: '12px', color: '#aaa', marginTop: '8px' },
  outputButtons: { display: 'flex', gap: '10px' },
  outputButton: {
    padding: '10px 24px',
    backgroundColor: '#F5F5F3',
    color: '#888',
    border: '1px solid #E8E8E4',
    borderRadius: '8px',
    fontSize: '14px',
    fontWeight: '500',
    cursor: 'pointer',
  },
  outputButtonActive: {
    backgroundColor: '#EDE9FE',
    color: '#7C3AED',
    border: '1px solid #C4B5FD',
  },
  generateButton: {
    width: '100%',
    padding: '14px',
    backgroundColor: '#C4B5FD',
    color: '#fff',
    border: 'none',
    borderRadius: '10px',
    fontSize: '15px',
    fontWeight: '600',
    cursor: 'pointer',
    marginTop: '8px',
  },
  resultHeader: {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: '16px',
  },
  sectionTitle: { fontSize: '18px', fontWeight: '700', color: '#2D2D2D' },
  resultButtons: { display: 'flex', gap: '10px' },
  resetButton: {
    padding: '8px 16px',
    backgroundColor: 'transparent',
    color: '#888',
    border: '1px solid #E8E8E4',
    borderRadius: '8px',
    fontSize: '13px',
    cursor: 'pointer',
  },
  downloadButton: {
    padding: '8px 16px',
    backgroundColor: '#C4B5FD',
    color: '#fff',
    border: 'none',
    borderRadius: '8px',
    fontSize: '13px',
    fontWeight: '600',
    cursor: 'pointer',
  },
  preview: {
    width: '100%',
    height: '800px',
    border: '1px solid #EFEFEB',
    borderRadius: '12px',
    backgroundColor: '#fff',
  },
};