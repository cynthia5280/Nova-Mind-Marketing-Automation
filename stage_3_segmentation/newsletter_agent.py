import os
import anthropic
from dotenv import load_dotenv

load_dotenv()

SYSTEM_PROMPT_HEAD = "You are writing a newsletter for the head of a social media agency managing 50-200 clients. They care about one thing: ROI. Speak to time saved, profit margin protected, and scaling without hiring. Use numbers. Make the business case. CTA: start a free NovaMind trial to reclaim 10+ hours per week."

SYSTEM_PROMPT_CREATIVE = "You are writing a newsletter for a creative (designer/copywriter) at a social media agency. They are overwhelmed by repetitive change requests — same design, different caption, 80 times over. They don't care about business metrics. They care about getting their creative energy back. Speak to the frustration of mindless repetition. CTA: show them NovaMind handles the repetitive requests so they can focus on actual creative work."

SYSTEM_PROMPT_PM = "You are writing a newsletter for a project manager at a social media agency juggling 50-200 client accounts. They live in Slack, email, and spreadsheets trying to track approvals, deadlines, and deliverables across every client. They need a system, not more tools. Speak to the chaos of multitasking and how NovaMind acts like an extra team member that never drops a ball. CTA: start a free trial."


def _call_claude(system_prompt: str, topic: str, draft: str) -> str:
    client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

    response = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=1024,
        system=system_prompt,
        messages=[
            {"role": "user", "content": f"Topic: {topic}\n\nBlog Draft:\n{draft}\n\nWrite a 150-200 word newsletter version."}
        ],
    )

    return response.content[0].text


def generate_newsletter_head(topic: str, draft: str) -> str:
    return _call_claude(SYSTEM_PROMPT_HEAD, topic, draft)


def generate_newsletter_creative(topic: str, draft: str) -> str:
    return _call_claude(SYSTEM_PROMPT_CREATIVE, topic, draft)


def generate_newsletter_pm(topic: str, draft: str) -> str:
    return _call_claude(SYSTEM_PROMPT_PM, topic, draft)
