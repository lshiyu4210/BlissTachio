from datetime import datetime, timedelta, timezone
from sqlalchemy.future import select
from backend.api.model import User, Message, WeeklySummary
import openai

async def generate_weekly_summaries(db):
    now = datetime.now(timezone.utc)
    week_end = now - timedelta(days=now.weekday())  # most recent Monday
    week_start = week_end - timedelta(days=7)

    result = await db.execute(select(User))
    users = result.scalars().all()

    for user in users:
        messages_result = await db.execute(
            select(Message).filter(
                Message.user_id == user.id,
                Message.timestamp >= week_start,
                Message.timestamp < week_end
            )
        )
        messages = [m.content for m in messages_result.scalars().all()]
        if not messages:
            continue

        summary_prompt = "\n".join(messages)
        response = openai.OpenAI(api_key="your-api-key").chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Summarize the user's weekly messages."},
                {"role": "user", "content": summary_prompt}
            ]
        )

        summary = WeeklySummary(
            user_id=user.id,
            week_start=week_start,
            week_end=week_end,
            summary=response.choices[0].message.content
        )
        db.add(summary)
        await db.commit()