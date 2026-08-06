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
                "role": "system",
                "content": "You are a resume analyzer. You must respond ONLY with the exact JSON format requested. Do not add any extra fields.",
            },
            {
                "role": "user",
                "content": f"""
다음 이력서를 분석해서 아래 JSON 형식으로만 반환해줘.
절대 다른 필드 추가하지 말고, 아래 형식 그대로만 출력해.

이력서:
{text[:3000]}

반드시 이 형식으로만 출력:
{{
    "skills": ["Java", "Spring", "MySQL"],
    "career": "신입",
    "job": "백엔드",
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