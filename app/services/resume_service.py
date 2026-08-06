import pdfplumber
import json
from io import BytesIO
from groq import Groq

from app.core.config import settings

client = Groq(api_key=settings.groq_api_key)


def extract_text_from_pdf(file_bytes: bytes) -> str:
    """
    PDF에서 텍스트를 추출합니다.
    """
    text = ""
    with pdfplumber.open(BytesIO(file_bytes)) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""
    return text


async def analyze_resume(text: str) -> dict:
    """
    이력서 텍스트를 AI로 분석합니다.
    """
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {
                "role": "user",
                "content": f"""
다음 이력서를 분석해서 JSON 형식으로 반환해줘.

이력서:
{text[:3000]}

출력 형식 (JSON만 출력, 다른 말 하지 말 것):
{{
    "skills": ["Java", "Spring", "MySQL"],
    "career": "신입 또는 경력 연차",
    "job": "적합한 직무 (예: 백엔드, 프론트엔드, 풀스택)",
    "summary": "이력서 한 줄 요약",
    "recommended_jobs": ["백엔드 개발자", "서버 개발자"],
    "missing_skills": ["Docker", "AWS"]
}}
""",
            }
        ],
        response_format={"type": "json_object"},
    )
    result = json.loads(response.choices[0].message.content)
    if isinstance(result, list):
        result = result[0] if result else {}
    return result