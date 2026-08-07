import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import client from '../api/client';

const EMPTY_PROJECT = {
  name: '',
  description: '',
  skills: '',
  github: '',
  deploy_url: '',
  period: '',
  image_filename: '',
};

export default function PortfolioPage() {
  const [step, setStep] = useState(1); // 1: 입력, 2: 미리보기
  const [output, setOutput] = useState('html');
  const [orientation, setOrientation] = useState('portrait');
  const [loading, setLoading] = useState(false);
  const [htmlResult, setHtmlResult] = useState(null);
  const [shareToken, setShareToken] = useState(null);
  const [pdfFiles, setPdfFiles] = useState([]);
  const [imageFiles, setImageFiles] = useState([]);
  const [form, setForm] = useState({
    name: '',
    job: '',
    email: '',
    phone: '',
    github: '',
    intro: '',
    skills: '',
    projects: [{ ...EMPTY_PROJECT }],
    experiences: [{ company: '', role: '', period: '', description: '' }],
    education: { school: '', major: '', graduation: '' },
  });
  const navigate = useNavigate();

  const handleFormChange = (field, value) => {
    setForm((prev) => ({ ...prev, [field]: value }));
  };

  const handleProjectChange = (index, field, value) => {
    const updated = [...form.projects];
    updated[index] = { ...updated[index], [field]: value };
    setForm((prev) => ({ ...prev, projects: updated }));
  };

  const handleExpChange = (index, field, value) => {
    const updated = [...form.experiences];
    updated[index] = { ...updated[index], [field]: value };
    setForm((prev) => ({ ...prev, experiences: updated }));
  };

  const handleGenerate = async () => {
    setLoading(true);
    try {
      const formData = new FormData();

      // PDF 파일들
      pdfFiles.forEach((f) => formData.append('files', f));
      // 이미지 파일들
      imageFiles.forEach((f) => formData.append('files', f));

      // 폼 데이터 JSON
      const portfolioData = {
        ...form,
        skills: form.skills.split(',').map((s) => s.trim()).filter(Boolean),
        projects: form.projects
          .filter((p) => p.name)
          .map((p) => ({
            ...p,
            skills: p.skills.split(',').map((s) => s.trim()).filter(Boolean),
          })),
        experiences: form.experiences.filter((e) => e.company),
      };

      formData.append('form_data', JSON.stringify(portfolioData));

      const res = await client.post(
        `/portfolio/generate?output=${output}&orientation=${orientation}`,
        formData,
        {
          headers: { 'Content-Type': 'multipart/form-data' },
          responseType: output === 'pdf' ? 'blob' : 'json',
        }
      );

      if (output === 'pdf') {
        const url = URL.createObjectURL(new Blob([res.data], { type: 'application/pdf' }));
        const a = document.createElement('a');
        a.href = url;
        a.download = 'portfolio.pdf';
        a.click();
      } else {
        setHtmlResult(res.data.html);
        setShareToken(res.data.share_token);
        setStep(2);
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
        {step === 2 && htmlResult ? (
          <div>
            <div style={styles.resultHeader}>
              <h2 style={styles.sectionTitle}>포트폴리오 미리보기</h2>
              <div style={styles.resultButtons}>
                <button style={styles.resetButton} onClick={() => setStep(1)}>
                  다시 만들기
                </button>
                {shareToken && (
                  <button
                    style={styles.shareButton}
                    onClick={() => {
                      const url = `${window.location.origin}/portfolio/share/${shareToken}`;
                      navigator.clipboard.writeText(url);
                      alert('링크가 복사됐습니다!');
                    }}
                  >
                    링크 복사
                  </button>
                )}
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
            <iframe srcDoc={htmlResult} style={styles.preview} title="포트폴리오 미리보기" />
          </div>
        ) : (
          <div style={styles.card}>
            <h1 style={styles.title}>포트폴리오 생성</h1>
            <p style={styles.subtitle}>정보를 입력하거나 이력서를 업로드해주세요.</p>

            {/* 파일 업로드 */}
            <div style={styles.section}>
              <p style={styles.sectionLabel}>파일 업로드</p>
              <div style={styles.fileRow}>
                <div>
                  <label style={styles.uploadLabel}>
                    <input
                      type="file"
                      accept=".pdf"
                      multiple
                      onChange={(e) => setPdfFiles(Array.from(e.target.files))}
                      style={{ display: 'none' }}
                    />
                    PDF 이력서 {pdfFiles.length > 0 && `(${pdfFiles.length}개)`}
                  </label>
                  <p style={styles.hint}>여러 개 선택 가능</p>
                </div>
                <div>
                  <label style={styles.uploadLabel}>
                    <input
                      type="file"
                      accept="image/*"
                      multiple
                      onChange={(e) => setImageFiles(Array.from(e.target.files))}
                      style={{ display: 'none' }}
                    />
                    프로젝트 이미지 {imageFiles.length > 0 && `(${imageFiles.length}개)`}
                  </label>
                  <p style={styles.hint}>프로젝트별 스크린샷</p>
                </div>
              </div>
            </div>

            {/* 기본 정보 */}
            <div style={styles.section}>
              <p style={styles.sectionLabel}>기본 정보</p>
              <div style={styles.grid2}>
                {[
                  { key: 'name', placeholder: '이름' },
                  { key: 'job', placeholder: '희망 직무' },
                  { key: 'email', placeholder: '이메일' },
                  { key: 'phone', placeholder: '전화번호' },
                  { key: 'github', placeholder: 'GitHub URL' },
                ].map(({ key, placeholder }) => (
                  <input
                    key={key}
                    style={styles.input}
                    placeholder={placeholder}
                    value={form[key]}
                    onChange={(e) => handleFormChange(key, e.target.value)}
                  />
                ))}
              </div>
              <textarea
                style={styles.textarea}
                placeholder="자기소개 (AI가 다듬어드립니다)"
                value={form.intro}
                onChange={(e) => handleFormChange('intro', e.target.value)}
              />
              <input
                style={styles.input}
                placeholder="기술스택 (쉼표로 구분: Java, Spring, React)"
                value={form.skills}
                onChange={(e) => handleFormChange('skills', e.target.value)}
              />
            </div>

            {/* 프로젝트 */}
            <div style={styles.section}>
              <div style={styles.sectionTop}>
                <p style={styles.sectionLabel}>프로젝트</p>
                <button
                  style={styles.addButton}
                  onClick={() =>
                    setForm((prev) => ({
                      ...prev,
                      projects: [...prev.projects, { ...EMPTY_PROJECT }],
                    }))
                  }
                >
                  + 추가
                </button>
              </div>
              {form.projects.map((project, i) => (
                <div key={i} style={styles.subCard}>
                  <div style={styles.subCardHeader}>
                    <span style={styles.subCardTitle}>프로젝트 {i + 1}</span>
                    {form.projects.length > 1 && (
                      <button
                        style={styles.removeButton}
                        onClick={() =>
                          setForm((prev) => ({
                            ...prev,
                            projects: prev.projects.filter((_, idx) => idx !== i),
                          }))
                        }
                      >
                        삭제
                      </button>
                    )}
                  </div>
                  <div style={styles.grid2}>
                    <input
                      style={styles.input}
                      placeholder="프로젝트명"
                      value={project.name}
                      onChange={(e) => handleProjectChange(i, 'name', e.target.value)}
                    />
                    <input
                      style={styles.input}
                      placeholder="기간 (예: 2024.01 ~ 2024.03)"
                      value={project.period}
                      onChange={(e) => handleProjectChange(i, 'period', e.target.value)}
                    />
                    <input
                      style={styles.input}
                      placeholder="GitHub URL"
                      value={project.github}
                      onChange={(e) => handleProjectChange(i, 'github', e.target.value)}
                    />
                    <input
                      style={styles.input}
                      placeholder="배포 URL"
                      value={project.deploy_url}
                      onChange={(e) => handleProjectChange(i, 'deploy_url', e.target.value)}
                    />
                  </div>
                  <input
                    style={styles.input}
                    placeholder="기술스택 (쉼표로 구분)"
                    value={project.skills}
                    onChange={(e) => handleProjectChange(i, 'skills', e.target.value)}
                  />
                  <textarea
                    style={styles.textarea}
                    placeholder="프로젝트 설명 (AI가 다듬어드립니다)"
                    value={project.description}
                    onChange={(e) => handleProjectChange(i, 'description', e.target.value)}
                  />
                  {imageFiles.length > 0 && (
                    <select
                      style={styles.input}
                      value={project.image_filename}
                      onChange={(e) => handleProjectChange(i, 'image_filename', e.target.value)}
                    >
                      <option value="">이미지 선택 (선택사항)</option>
                      {imageFiles.map((f) => (
                        <option key={f.name} value={f.name}>{f.name}</option>
                      ))}
                    </select>
                  )}
                </div>
              ))}
            </div>

            {/* 경력 */}
            <div style={styles.section}>
              <div style={styles.sectionTop}>
                <p style={styles.sectionLabel}>경력</p>
                <button
                  style={styles.addButton}
                  onClick={() =>
                    setForm((prev) => ({
                      ...prev,
                      experiences: [...prev.experiences, { company: '', role: '', period: '', description: '' }],
                    }))
                  }
                >
                  + 추가
                </button>
              </div>
              {form.experiences.map((exp, i) => (
                <div key={i} style={styles.subCard}>
                  <div style={styles.subCardHeader}>
                    <span style={styles.subCardTitle}>경력 {i + 1}</span>
                    {form.experiences.length > 1 && (
                      <button
                        style={styles.removeButton}
                        onClick={() =>
                          setForm((prev) => ({
                            ...prev,
                            experiences: prev.experiences.filter((_, idx) => idx !== i),
                          }))
                        }
                      >
                        삭제
                      </button>
                    )}
                  </div>
                  <div style={styles.grid2}>
                    <input style={styles.input} placeholder="회사명" value={exp.company} onChange={(e) => handleExpChange(i, 'company', e.target.value)} />
                    <input style={styles.input} placeholder="직책" value={exp.role} onChange={(e) => handleExpChange(i, 'role', e.target.value)} />
                    <input style={styles.input} placeholder="기간" value={exp.period} onChange={(e) => handleExpChange(i, 'period', e.target.value)} />
                  </div>
                  <textarea style={styles.textarea} placeholder="업무 설명" value={exp.description} onChange={(e) => handleExpChange(i, 'description', e.target.value)} />
                </div>
              ))}
            </div>

            {/* 학력 */}
            <div style={styles.section}>
              <p style={styles.sectionLabel}>학력</p>
              <div style={styles.grid2}>
                <input style={styles.input} placeholder="학교명" value={form.education.school} onChange={(e) => setForm((prev) => ({ ...prev, education: { ...prev.education, school: e.target.value } }))} />
                <input style={styles.input} placeholder="전공" value={form.education.major} onChange={(e) => setForm((prev) => ({ ...prev, education: { ...prev.education, major: e.target.value } }))} />
                <input style={styles.input} placeholder="졸업일 (예: 2024.02)" value={form.education.graduation} onChange={(e) => setForm((prev) => ({ ...prev, education: { ...prev.education, graduation: e.target.value } }))} />
              </div>
            </div>

            {/* 출력 설정 */}
            <div style={styles.section}>
              <p style={styles.sectionLabel}>출력 설정</p>
              <div style={styles.outputRow}>
                <div>
                  <p style={styles.hint}>형식</p>
                  <div style={styles.outputButtons}>
                    {['html', 'pdf'].map((o) => (
                      <button
                        key={o}
                        style={{ ...styles.outputButton, ...(output === o ? styles.outputButtonActive : {}) }}
                        onClick={() => setOutput(o)}
                      >
                        {o.toUpperCase()}
                      </button>
                    ))}
                  </div>
                </div>
                <div>
                  <p style={styles.hint}>방향</p>
                  <div style={styles.outputButtons}>
                    {[{ key: 'portrait', label: '세로' }, { key: 'landscape', label: '가로' }].map(({ key, label }) => (
                      <button
                        key={key}
                        style={{ ...styles.outputButton, ...(orientation === key ? styles.outputButtonActive : {}) }}
                        onClick={() => setOrientation(key)}
                      >
                        {label}
                      </button>
                    ))}
                  </div>
                </div>
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
  header: { backgroundColor: '#fff', borderBottom: '1px solid #EFEFEB', position: 'sticky', top: 0, zIndex: 100 },
  headerInner: { maxWidth: '1100px', margin: '0 auto', padding: '0 24px', height: '64px', display: 'flex', alignItems: 'center', justifyContent: 'space-between' },
  headerLeft: { display: 'flex', alignItems: 'center', gap: '12px' },
  logo: { width: '36px', height: '36px', borderRadius: '10px', backgroundColor: '#C4B5FD', color: '#fff', display: 'flex', alignItems: 'center', justifyContent: 'center', fontWeight: '700', fontSize: '13px' },
  headerTitle: { fontSize: '15px', fontWeight: '600', color: '#2D2D2D' },
  backButton: { padding: '8px 18px', backgroundColor: 'transparent', color: '#888', border: '1px solid #E8E8E4', borderRadius: '8px', fontSize: '13px', cursor: 'pointer' },
  main: { maxWidth: '760px', margin: '0 auto', padding: '40px 24px' },
  card: { backgroundColor: '#fff', borderRadius: '20px', padding: '40px', border: '1px solid #EFEFEB' },
  title: { fontSize: '22px', fontWeight: '700', color: '#2D2D2D', marginBottom: '6px' },
  subtitle: { fontSize: '14px', color: '#888', marginBottom: '32px' },
  section: { marginBottom: '28px', paddingBottom: '28px', borderBottom: '1px solid #EFEFEB' },
  sectionTop: { display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '16px' },
  sectionLabel: { fontSize: '13px', fontWeight: '600', color: '#555', marginBottom: '12px', textTransform: 'uppercase', letterSpacing: '0.05em' },
  grid2: { display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '10px', marginBottom: '10px' },
  input: { padding: '11px 14px', borderRadius: '8px', border: '1.5px solid #E8E8E4', fontSize: '13px', backgroundColor: '#FAFAF7', outline: 'none', width: '100%' },
  textarea: { padding: '11px 14px', borderRadius: '8px', border: '1.5px solid #E8E8E4', fontSize: '13px', backgroundColor: '#FAFAF7', outline: 'none', width: '100%', minHeight: '80px', resize: 'vertical', marginTop: '10px', fontFamily: 'inherit' },
  fileRow: { display: 'flex', gap: '16px', flexWrap: 'wrap' },
  uploadLabel: { display: 'inline-block', padding: '10px 18px', backgroundColor: '#F5F3FF', color: '#7C3AED', borderRadius: '8px', fontSize: '13px', fontWeight: '600', cursor: 'pointer', border: '1px solid #C4B5FD' },
  hint: { fontSize: '12px', color: '#aaa', marginTop: '6px' },
  subCard: { backgroundColor: '#FAFAF7', borderRadius: '12px', padding: '16px', marginBottom: '12px' },
  subCardHeader: { display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '12px' },
  subCardTitle: { fontSize: '13px', fontWeight: '600', color: '#555' },
  addButton: { padding: '6px 14px', backgroundColor: '#EDE9FE', color: '#7C3AED', border: 'none', borderRadius: '6px', fontSize: '12px', fontWeight: '600', cursor: 'pointer' },
  removeButton: { padding: '4px 10px', backgroundColor: 'transparent', color: '#aaa', border: '1px solid #E8E8E4', borderRadius: '6px', fontSize: '12px', cursor: 'pointer' },
  outputRow: { display: 'flex', gap: '32px', flexWrap: 'wrap' },
  outputButtons: { display: 'flex', gap: '8px', marginTop: '8px' },
  outputButton: { padding: '8px 20px', backgroundColor: '#F5F5F3', color: '#888', border: '1px solid #E8E8E4', borderRadius: '8px', fontSize: '13px', cursor: 'pointer' },
  outputButtonActive: { backgroundColor: '#EDE9FE', color: '#7C3AED', border: '1px solid #C4B5FD' },
  generateButton: { width: '100%', padding: '14px', backgroundColor: '#C4B5FD', color: '#fff', border: 'none', borderRadius: '10px', fontSize: '15px', fontWeight: '600', cursor: 'pointer', marginTop: '8px' },
  resultHeader: { display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '16px' },
  sectionTitle: { fontSize: '18px', fontWeight: '700', color: '#2D2D2D' },
  resultButtons: { display: 'flex', gap: '10px' },
  resetButton: { padding: '8px 16px', backgroundColor: 'transparent', color: '#888', border: '1px solid #E8E8E4', borderRadius: '8px', fontSize: '13px', cursor: 'pointer' },
  shareButton: { padding: '8px 16px', backgroundColor: '#F5F3FF', color: '#7C3AED', border: '1px solid #C4B5FD', borderRadius: '8px', fontSize: '13px', fontWeight: '600', cursor: 'pointer' },
  downloadButton: { padding: '8px 16px', backgroundColor: '#C4B5FD', color: '#fff', border: 'none', borderRadius: '8px', fontSize: '13px', fontWeight: '600', cursor: 'pointer' },
  preview: { width: '100%', height: '800px', border: '1px solid #EFEFEB', borderRadius: '12px', backgroundColor: '#fff' },
};