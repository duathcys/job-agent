# 🎯 취업 준비 AI 에이전트

> 채용공고를 자동으로 수집하고, AI가 분석해서 나에게 맞는 공고를 추천해주는 서비스

## 🔗 배포 URL

| 서비스 | URL |
|--------|-----|
| 프론트엔드 | https://job-agent-9c0lnso5m-duathcys.vercel.app |
| 백엔드 API | https://job-agent-backend-u9d2.onrender.com |
| API 문서 | https://job-agent-backend-u9d2.onrender.com/docs |

---

## 📌 프로젝트 소개

취업 준비생이 채용공고를 놓치지 않고, 자신에게 맞는 공고를 빠르게 찾을 수 있도록 도와주는 AI 에이전트입니다.

사용자가 희망 직무, 기술스택, 관심 기업을 입력하면 AI가 매일 채용공고를 수집하고 적합도를 분석해서 이메일로 알려줍니다.

---

## 🏗️ 시스템 아키텍처

```
React (Vercel)
      ↓
FastAPI (Render)
      ↓
LangGraph Agent
  ├─ 원티드 크롤링
  ├─ AI 공고 요약 (Groq)
  ├─ 적합도 계산 (Groq)
  └─ 이메일 발송 (Gmail SMTP)
      ↓
PostgreSQL (Supabase)
```

---

## ✨ 주요 기능

### 1. 채용공고 자동 수집
- 원티드 비공식 API를 활용한 실시간 공고 수집
- 중복 공고 자동 필터링
- 매일 오전 9시 자동 실행 (APScheduler)

### 2. AI 공고 요약
- Groq LLM을 활용한 공고 자동 요약
- 회사, 직무, 주요업무, 필수기술, 우대사항, 마감일 구조화

### 3. 적합도 분석
- 사용자 기술스택과 공고 요구 기술 비교
- 0~100% 적합도 점수 산출
- 보유 기술 / 부족한 기술 분석

### 4. 이메일 알림
- 에이전트 실행 완료 후 가입 이메일로 추천 공고 발송
- HTML 이메일 템플릿

### 5. LangGraph Agent
- 크롤링 → 요약 → 적합도 계산 → 추천 파이프라인 자동화
- 에러 발생 시 자동 중단

---

## 🛠️ 기술 스택

### Backend
| 기술 | 용도 |
|------|------|
| FastAPI | REST API 서버 |
| SQLAlchemy | ORM |
| PostgreSQL | 데이터베이스 |
| LangGraph | AI Agent 파이프라인 |
| Groq (LLaMA 3) | LLM 공고 요약 / 적합도 분석 |
| APScheduler | 스케줄러 |
| JWT | 인증 |
| pytest | 테스트 |

### Frontend
| 기술 | 용도 |
|------|------|
| React | UI |
| Vite | 빌드 도구 |
| React Router | 라우팅 |
| Axios | HTTP 클라이언트 |

### Infrastructure
| 기술 | 용도 |
|------|------|
| Supabase | PostgreSQL DB 호스팅 |
| Render | 백엔드 배포 |
| Vercel | 프론트엔드 배포 |
| Docker | 컨테이너화 |

---

## 📁 프로젝트 구조

```
job-agent/
├── app/
│   ├── api/v1/endpoints/    # API 엔드포인트
│   ├── core/                # 설정, 인증, 의존성
│   ├── db/                  # DB 연결
│   ├── models/              # SQLAlchemy 모델
│   ├── repositories/        # DB 쿼리
│   ├── schemas/             # Pydantic 스키마
│   └── services/            # 비즈니스 로직
├── agent/
│   ├── nodes/               # LangGraph 노드
│   ├── graph.py             # Agent 그래프
│   └── state.py             # Agent 상태
├── crawler/
│   └── wanted.py            # 원티드 크롤러
├── frontend/                # React 앱
├── tests/                   # pytest 테스트
├── Dockerfile
├── docker-compose.yml
└── requirements.txt
```

---

## 🚀 로컬 실행 방법

### 1. 레포 클론
```bash
git clone https://github.com/duathcys/job-agent.git
cd job-agent
```

### 2. 가상환경 설정
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3. 환경변수 설정
```bash
cp .env.example .env
# .env 파일에 값 입력
```

```
DATABASE_URL=postgresql://...
SECRET_KEY=your-secret-key
GROQ_API_KEY=your-groq-api-key
GMAIL_USER=your-gmail@gmail.com
GMAIL_PASSWORD=your-app-password
```

### 4. 백엔드 실행
```bash
uvicorn app.main:app --reload
```

### 5. 프론트엔드 실행
```bash
cd frontend
npm install
npm run dev
```

### 6. Docker로 실행
```bash
docker-compose up --build
```

---

## 🧪 테스트 실행

```bash
pytest -v
```

---

## 📮 API 문서

서버 실행 후 아래 URL에서 Swagger UI 확인 가능합니다.

```
http://localhost:8000/docs
```

### 주요 엔드포인트

| Method | URL | 설명 |
|--------|-----|------|
| POST | /api/v1/users/ | 회원가입 |
| POST | /api/v1/auth/login | 로그인 |
| POST | /api/v1/agent/run | AI 에이전트 실행 |
| GET | /api/v1/agent/recommendations | 추천 공고 조회 |
| POST | /api/v1/jobs/{id}/summarize | 공고 AI 요약 |
| POST | /api/v1/jobs/{id}/fit-score | 적합도 계산 |

---

## 🔄 AI Agent 흐름

```
START
  ↓
[1] 크롤링 노드
  └─ 원티드에서 최신 공고 수집
  └─ DB 저장 (중복 제외)
  ↓
[2] 요약 노드
  └─ Groq LLM으로 공고 요약
  └─ 한 줄 요약 생성
  ↓
[3] 적합도 계산 노드
  └─ 사용자 스킬 vs 공고 요구 기술 비교
  └─ 0~100% 점수 산출
  ↓
[4] 추천 노드
  └─ 적합도 상위 5개 선별
  └─ 이메일 발송
  ↓
END
```

---

## 👨‍💻 개발자

- GitHub: [@duathcys](https://github.com/duathcys)