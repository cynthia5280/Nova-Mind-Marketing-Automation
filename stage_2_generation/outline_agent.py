import os
import anthropic
from dotenv import load_dotenv

load_dotenv()

SYSTEM_PROMPT = "You are a content strategist for NovaMind, a workflow automation tool built for social media agencies. Our readers manage 50-200 clients and are drowning in repetitive work — writing captions, chasing approvals, sending calendars, pulling reports — multiplied across every client. They're considering hiring more people but that destroys ROI. They are skeptical of AI. Lead with the operational pain. Use real, specific examples. Build the case slowly before introducing NovaMind as the solution. The goal is to get them to start a free trial. Write a 5-section blog outline with a headline and one sentence per section."


def generate_outline(topic: str, audience: str, intent: str) -> str:
    client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

    response = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=1024,
        system=SYSTEM_PROMPT,
        messages=[
            {"role": "user", "content": f"Topic: {topic}\nAudience: {audience}\nIntent: {intent}"}
        ],
    )

    return response.content[0].text
