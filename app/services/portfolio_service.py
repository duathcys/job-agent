import json
from groq import Groq
from app.core.config import settings

client = Groq(api_key=settings.groq_api_key)


async def enhance_portfolio(data: dict) -> dict:
    """
    포트폴리오 내용을 AI로 다듬어줍니다.
    """
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {
                "role": "system",
                "content": "You are a professional portfolio writer. Enhance the given portfolio data to make it more impressive and professional. Respond only in JSON format.",
            },
            {
                "role": "user",
                "content": f"""
다음 포트폴리오 정보를 더 전문적이고 인상적으로 다듬어줘.
각 프로젝트 설명은 임팩트 있게, 기술스택은 정리해서, 자기소개는 매력적으로 만들어줘.

포트폴리오 정보:
{json.dumps(data, ensure_ascii=False, indent=2)}

반드시 이 형식으로만 출력:
{{
    "name": "이름",
    "job": "직무",
    "email": "이메일",
    "phone": "전화번호",
    "github": "GitHub URL",
    "intro": "매력적인 자기소개 2-3문장",
    "skills": ["기술1", "기술2"],
    "projects": [
        {{
            "name": "프로젝트명",
            "description": "임팩트 있는 프로젝트 설명 2-3문장",
            "skills": ["기술1", "기술2"],
            "github": "GitHub URL",
            "period": "기간"
        }}
    ],
    "experiences": [
        {{
            "company": "회사명",
            "role": "직책",
            "period": "기간",
            "description": "업무 설명"
        }}
    ],
    "education": {{
        "school": "학교명",
        "major": "전공",
        "graduation": "졸업일"
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


def generate_html(data: dict) -> str:
    """
    포트폴리오 HTML을 생성합니다.
    """
    projects_html = ""
    for project in data.get("projects", []):
        skills_html = "".join([
            f'<span class="skill-tag">{skill}</span>'
            for skill in project.get("skills", [])
        ])
        projects_html += f"""
        <div class="project-card">
            <div class="project-header">
                <h3>{project.get("name", "")}</h3>
                <span class="period">{project.get("period", "")}</span>
            </div>
            <p>{project.get("description", "")}</p>
            <div class="skills">{skills_html}</div>
            {f'<a href="{project["github"]}" class="github-link">GitHub →</a>' if project.get("github") else ""}
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
            font-family: 'Pretendard', -apple-system, BlinkMacSystemFont, sans-serif;
            background: #FAFAF7;
            color: #2D2D2D;
            line-height: 1.6;
        }}
        .container {{ max-width: 860px; margin: 0 auto; padding: 60px 40px; }}

        /* 헤더 */
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
        .name {{ font-size: 32px; font-weight: 700; color: #2D2D2D; }}
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

        /* 섹션 */
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

        /* 기술스택 */
        .skills {{ display: flex; flex-wrap: wrap; gap: 8px; }}
        .skill-tag {{
            background: #F5F3FF;
            color: #7C3AED;
            padding: 6px 14px;
            border-radius: 8px;
            font-size: 13px;
            font-weight: 500;
        }}

        /* 프로젝트 */
        .project-card {{
            padding: 20px 0;
            border-bottom: 1px solid #EFEFEB;
        }}
        .project-card:last-child {{ border-bottom: none; padding-bottom: 0; }}
        .project-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 8px;
        }}
        .project-header h3 {{ font-size: 16px; font-weight: 600; }}
        .github-link {{
            color: #7C3AED;
            font-size: 13px;
            text-decoration: none;
            margin-top: 8px;
            display: inline-block;
        }}

        /* 경력 */
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

        /* 공통 */
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


def generate_pdf(data: dict) -> bytes:
    """
    포트폴리오 PDF를 생성합니다.
    """
    from weasyprint import HTML, CSS
    import os

    font_dir = os.path.join(os.path.dirname(__file__), "../static/fonts")
    font_regular = os.path.join(font_dir, "NotoSansKR-Regular.ttf")
    font_bold = os.path.join(font_dir, "NotoSansKR-Bold.ttf")

    html_content = generate_html(data)

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
        body {{
            font-family: 'NotoSansKR', sans-serif !important;
        }}
    """)

    return HTML(string=html_content).write_pdf(stylesheets=[font_css])