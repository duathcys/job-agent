import resend
from app.core.config import settings


def send_recommendation_email(to_email: str, jobs: list[dict]):
    """
    추천 공고를 이메일로 발송합니다.
    """
    if not settings.resend_api_key:
        print("Resend API 키가 없어 발송을 건너뜁니다.")
        return

    resend.api_key = settings.resend_api_key

    html = f"""
    <html>
    <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px;">
        <h1 style="color: #4F46E5;">🎯 오늘의 맞춤 채용공고</h1>
        <p>안녕하세요! AI 에이전트가 분석한 맞춤 공고를 보내드립니다.</p>
        <hr/>
        {"".join([f'''
        <div style="border: 1px solid #eee; border-radius: 8px; padding: 16px; margin: 16px 0;">
            <div style="display: flex; justify-content: space-between;">
                <h3 style="margin: 0; color: #333;">{job["company"]}</h3>
                <span style="background: #EEF2FF; color: #4F46E5; padding: 4px 10px; border-radius: 20px; font-size: 13px;">
                    적합도 {job["fit_score"]}%
                </span>
            </div>
            <p style="color: #555; margin: 8px 0;">{job["title"]}</p>
            <p style="color: #777; font-size: 13px;">{job.get("summary", "")}</p>
            {f'<p style="color: #e57373; font-size: 13px;">⏰ 마감일: {job["deadline"]}</p>' if job.get("deadline") else ""}
            <a href="{job["url"]}" style="color: #4F46E5; font-size: 14px;">공고 보러가기 →</a>
        </div>
        ''' for job in jobs])}
        <hr/>
        <p style="color: #aaa; font-size: 12px;">취업 AI 에이전트가 발송한 메일입니다.</p>
    </body>
    </html>
    """

    try:
        resend.Emails.send({
            "from": "onboarding@resend.dev",
            "to": to_email,
            "subject": "🎯 오늘의 맞춤 채용공고 추천",
            "html": html,
        })
        print(f"✅ 이메일 발송 완료: {to_email}")
    except Exception as e:
        print(f"❌ 이메일 발송 실패: {e}")
        import traceback
        traceback.print_exc()