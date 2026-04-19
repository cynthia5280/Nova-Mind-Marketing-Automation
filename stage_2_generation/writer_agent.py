import os
import anthropic
from dotenv import load_dotenv

load_dotenv()

SYSTEM_PROMPT = "You are a content writer for NovaMind, a workflow automation tool for social media agencies. Write like a consultant who deeply understands the day-to-day pain of running a social media agency — not a tech blogger. Avoid generic AI hype and vague introductions. Open with a specific, relatable scenario (e.g. three people spending 10 hours a week manually building and sending content calendars to 80 clients). Use concrete numbers and real agency situations throughout. Structure: start with the pain (specific and vivid), then show how NovaMind solves it with a concrete before/after example, then close with a clear CTA to start a free trial. Write a 400-600 word blog post draft based on the outline provided. Do not use corporate language. Sound like someone who has sat in their office and watched them suffer."


def generate_draft(topic: str, audience: str, intent: str, outline: str) -> str:
    client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

    response = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=2048,
        system=SYSTEM_PROMPT,
        messages=[
            {"role": "user", "content": f"Topic: {topic}\nAudience: {audience}\nIntent: {intent}\n\nOutline:\n{outline}"}
        ],
    )

    return response.content[0].text
