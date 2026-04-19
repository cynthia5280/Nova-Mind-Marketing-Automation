import os
import random
import anthropic
from dotenv import load_dotenv

load_dotenv()

SYSTEM_PROMPT = "You are a marketing analyst reviewing newsletter campaign performance for a social media agency tool called NovaMind. You will be given performance metrics across three audience personas. Write a brief 3-4 sentence analysis comparing performance across personas and give one specific, actionable content recommendation for next week. Be direct and data-driven."


def _simulate_metrics() -> dict:
    return {
        "open_rate": round(random.uniform(0.25, 0.45), 4),
        "click_rate": round(random.uniform(0.03, 0.08), 4),
        "unsubscribe_rate": round(random.uniform(0.001, 0.005), 4),
    }


def generate_report(topic: str, newsletters: dict) -> dict:
    metrics = {
        "head": _simulate_metrics(),
        "creative": _simulate_metrics(),
        "pm": _simulate_metrics(),
    }

    metrics_summary = "\n".join(
        f"{persona.upper()}: open={m['open_rate']:.1%}, click={m['click_rate']:.1%}, unsub={m['unsubscribe_rate']:.2%}"
        for persona, m in metrics.items()
    )

    client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

    response = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=512,
        system=SYSTEM_PROMPT,
        messages=[
            {
                "role": "user",
                "content": (
                    f"Topic: {topic}\n\n"
                    f"Performance Metrics:\n{metrics_summary}\n\n"
                    f"Newsletter previews:\n"
                    f"HEAD: {newsletters['head'][:300]}\n"
                    f"CREATIVE: {newsletters['creative'][:300]}\n"
                    f"PM: {newsletters['pm'][:300]}"
                ),
            }
        ],
    )

    return {
        "metrics": metrics,
        "ai_analysis": response.content[0].text,
    }
