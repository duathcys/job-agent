import json
import base64
from groq import Groq
from app.core.config import settings

client = Groq(api_key=settings.groq_api_key)


async def enhance_portfolio(data: dict) -> dict:
    clean_data = {k: v for k, v in data.items() if k != "raw_resume"}

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": """You are a professional portfolio writer.
CRITICAL RULES:
1. Respond ONLY with valid JSON. No markdown, no backticks.
2. NEVER invent or fabricate any information.
3. If a field is empty or missing, keep it as empty string or empty array.
4. Only enhance the writing style of existing content, do not add new facts.""",
            },
            {
                "role": "user",
                "content": f"""
아래 포트폴리오 정보의 문장을 더 전문적으로 다듬어줘.
절대 없는 정보를 지어내지 마. 비어있는 필드는 그대로 비워둬.
기존 데이터는 반드시 유지하고 문체만 다듬어줘.

입력:
{json.dumps(clean_data, ensure_ascii=False, indent=2)[:2000]}

출력 형식:
{{
    "name": "입력된 이름 그대로",
    "job": "입력된 직무 그대로",
    "email": "입력된 이메일 그대로",
    "phone": "입력된 전화번호 그대로",
    "github": "입력된 github 그대로",
    "intro": "입력된 자기소개를 더 매력적으로 다듬기 (없으면 빈 문자열)",
    "skills": ["입력된 기술 그대로"],
    "projects": [
        {{
            "name": "입력된 프로젝트명 그대로",
            "description": "입력된 설명을 더 임팩트 있게 다듬기 (없으면 빈 문자열)",
            "skills": ["입력된 기술 그대로"],
            "github": "입력된 github 그대로",
            "deploy_url": "입력된 deploy_url 그대로",
            "period": "입력된 기간 그대로",
            "image": null
        }}
    ],
    "experiences": [
        {{
            "company": "입력된 회사명 그대로",
            "role": "입력된 직책 그대로",
            "period": "입력된 기간 그대로",
            "description": "입력된 설명을 더 전문적으로 다듬기 (없으면 빈 문자열)"
        }}
    ],
    "education": {{
        "school": "입력된 학교 그대로",
        "major": "입력된 전공 그대로",
        "graduation": "입력된 졸업일 그대로"
    }}
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


def image_to_base64(image_bytes: bytes, content_type: str) -> str:
    """이미지를 base64로 변환합니다."""
    encoded = base64.b64encode(image_bytes).decode("utf-8")
    return f"data:{content_type};base64,{encoded}"


def generate_html(data: dict, orientation: str = "portrait") -> str:
    """
    포트폴리오 HTML을 생성합니다.
    orientation: portrait(세로) 또는 landscape(가로)
    """
    max_width = "860px" if orientation == "portrait" else "1100px"

    projects_html = ""
    for project in data.get("projects", []):
        skills_html = "".join([
            f'<span class="skill-tag">{skill}</span>'
            for skill in project.get("skills", [])
        ])
        image_html = ""
        if project.get("image"):
            image_html = f'<img src="{project["image"]}" class="project-image" alt="{project.get("name", "")}" />'

        links_html = ""
        if project.get("github"):
            links_html += f'<a href="{project["github"]}" class="project-link">GitHub →</a>'
        if project.get("deploy_url"):
            links_html += f'<a href="{project["deploy_url"]}" class="project-link">배포 →</a>'

        projects_html += f"""
        <div class="project-card">
            {image_html}
            <div class="project-header">
                <h3>{project.get("name", "")}</h3>
                <span class="period">{project.get("period", "")}</span>
            </div>
            <p>{project.get("description", "")}</p>
            <div class="skills">{skills_html}</div>
            <div class="project-links">{links_html}</div>
        </div>
        """

    experiences_html = ""
    for exp in data.get("experiences", []):
        experiences_html += f"""
        <div class="experience-item">
            <div class="exp-header">
                <strong>{exp.get("company", "")}</strong>
                <span class="period">{exp.get("period", "")}</span>
            </div>
            <p class="role">{exp.get("role", "")}</p>
            <p>{exp.get("description", "")}</p>
        </div>
        """

    skills_html = "".join([
        f'<span class="skill-tag">{skill}</span>'
        for skill in data.get("skills", [])
    ])

    education = data.get("education", {})

    return f"""
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{data.get("name", "")} 포트폴리오</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;500;600;700&display=swap" rel="stylesheet">
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: 'Noto Sans KR', -apple-system, sans-serif;
            background: #FAFAF7;
            color: #2D2D2D;
            line-height: 1.6;
        }}
        .container {{ max-width: {max_width}; margin: 0 auto; padding: 60px 40px; }}
        .header {{
            background: #fff;
            border-radius: 20px;
            padding: 40px;
            margin-bottom: 24px;
            border: 1px solid #EFEFEB;
        }}
        .header-top {{
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            margin-bottom: 20px;
        }}
        .name {{ font-size: 32px; font-weight: 700; }}
        .job-badge {{
            background: #EDE9FE;
            color: #7C3AED;
            padding: 6px 16px;
            border-radius: 20px;
            font-size: 14px;
            font-weight: 600;
        }}
        .intro {{ font-size: 15px; color: #555; margin-bottom: 20px; line-height: 1.8; }}
        .contacts {{ display: flex; gap: 16px; flex-wrap: wrap; }}
        .contact-item {{ font-size: 13px; color: #888; }}
        .contact-item a {{ color: #7C3AED; text-decoration: none; }}
        .section {{
            background: #fff;
            border-radius: 20px;
            padding: 32px 40px;
            margin-bottom: 24px;
            border: 1px solid #EFEFEB;
        }}
        .section-title {{
            font-size: 13px;
            font-weight: 600;
            color: #888;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            margin-bottom: 20px;
        }}
        .skills {{ display: flex; flex-wrap: wrap; gap: 8px; }}
        .skill-tag {{
            background: #F5F3FF;
            color: #7C3AED;
            padding: 6px 14px;
            border-radius: 8px;
            font-size: 13px;
            font-weight: 500;
        }}
        .project-card {{
            padding: 24px 0;
            border-bottom: 1px solid #EFEFEB;
        }}
        .project-card:last-child {{ border-bottom: none; padding-bottom: 0; }}
        .project-image {{
            width: 100%;
            max-height: 240px;
            object-fit: cover;
            border-radius: 10px;
            margin-bottom: 16px;
        }}
        .project-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 8px;
        }}
        .project-header h3 {{ font-size: 16px; font-weight: 600; }}
        .project-links {{ display: flex; gap: 12px; margin-top: 10px; }}
        .project-link {{
            color: #7C3AED;
            font-size: 13px;
            text-decoration: none;
            font-weight: 500;
        }}
        .experience-item {{
            padding: 16px 0;
            border-bottom: 1px solid #EFEFEB;
        }}
        .experience-item:last-child {{ border-bottom: none; padding-bottom: 0; }}
        .exp-header {{
            display: flex;
            justify-content: space-between;
            margin-bottom: 4px;
        }}
        .role {{ color: #7C3AED; font-size: 13px; margin-bottom: 6px; }}
        .period {{ font-size: 12px; color: #aaa; }}
        p {{ font-size: 14px; color: #555; margin-top: 6px; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div class="header-top">
                <h1 class="name">{data.get("name", "")}</h1>
                <span class="job-badge">{data.get("job", "")}</span>
            </div>
            <p class="intro">{data.get("intro", "")}</p>
            <div class="contacts">
                {f'<span class="contact-item">{data.get("email", "")}</span>' if data.get("email") else ""}
                {f'<span class="contact-item">{data.get("phone", "")}</span>' if data.get("phone") else ""}
                {f'<span class="contact-item"><a href="{data.get("github")}">GitHub</a></span>' if data.get("github") else ""}
            </div>
        </div>

        <div class="section">
            <p class="section-title">기술스택</p>
            <div class="skills">{skills_html}</div>
        </div>

        {f'''<div class="section">
            <p class="section-title">프로젝트</p>
            {projects_html}
        </div>''' if data.get("projects") else ""}

        {f'''<div class="section">
            <p class="section-title">경력</p>
            {experiences_html}
        </div>''' if data.get("experiences") else ""}

        {f'''<div class="section">
            <p class="section-title">학력</p>
            <div class="experience-item">
                <div class="exp-header">
                    <strong>{education.get("school", "")}</strong>
                    <span class="period">{education.get("graduation", "")}</span>
                </div>
                <p class="role">{education.get("major", "")}</p>
            </div>
        </div>''' if education else ""}
    </div>
</body>
</html>
"""


def generate_pdf(data: dict, orientation: str = "portrait") -> bytes:
    """포트폴리오 PDF를 생성합니다."""
    from weasyprint import HTML, CSS
    import os

    font_dir = os.path.join(os.path.dirname(__file__), "../static/fonts")
    font_regular = os.path.join(font_dir, "NotoSansKR-Regular.ttf")
    font_bold = os.path.join(font_dir, "NotoSansKR-Bold.ttf")

    page_size = "A4 landscape" if orientation == "landscape" else "A4"

    html_content = generate_html(data, orientation)
    font_css = CSS(string=f"""
        @font-face {{
            font-family: 'NotoSansKR';
            src: url('file://{font_regular}');
            font-weight: 400;
        }}
        @font-face {{
            font-family: 'NotoSansKR';
            src: url('file://{font_bold}');
            font-weight: 700;
        }}
        @page {{ size: {page_size}; margin: 0; }}
        body {{ font-family: 'NotoSansKR', sans-serif !important; }}
    """)
    return HTML(string=html_content).write_pdf(stylesheets=[font_css])