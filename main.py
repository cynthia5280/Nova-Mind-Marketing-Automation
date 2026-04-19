import os
import json
from datetime import datetime
from dotenv import load_dotenv
import anthropic
from stage_2_generation.outline_agent import generate_outline
from stage_2_generation.writer_agent import generate_draft
from stage_3_segmentation.newsletter_agent import (
    generate_newsletter_head,
    generate_newsletter_creative,
    generate_newsletter_pm,
)
from stage_4_distribution.hubspot_agent import distribute_to_hubspot
from stage_5_reporting.report_agent import generate_report
from stage_5_reporting.html_report import generate_html_report

load_dotenv()

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))


def collect_inputs():
    print("\n=== AI Content Automation Pipeline ===\n")
    topic = input("Blog topic: ").strip()
    audience = input("Target audience description: ").strip()
    intent = input("Content intent: ").strip()
    return {"topic": topic, "audience": audience, "intent": intent}


def run_pipeline():
    inputs = collect_inputs()

    print("\n--- Collected Inputs ---")
    print(f"Topic:    {inputs['topic']}")
    print(f"Audience: {inputs['audience']}")
    print(f"Intent:   {inputs['intent']}")
    print("------------------------\n")

    # Stage 2: Generation
    print("Generating outline...\n")
    outline = generate_outline(inputs["topic"], inputs["audience"], inputs["intent"])
    print("--- Outline ---")
    print(outline)

    print("Generating draft...\n")
    draft = generate_draft(inputs["topic"], inputs["audience"], inputs["intent"], outline)
    print("--- Draft ---")
    print(draft)

    # Stage 3: Segmentation
    print("Generating newsletters...\n")

    print("--- HEAD OF AGENCY ---")
    newsletter_head = generate_newsletter_head(inputs["topic"], draft)
    print(newsletter_head)

    print("--- CREATIVES ---")
    newsletter_creative = generate_newsletter_creative(inputs["topic"], draft)
    print(newsletter_creative)

    print("--- PM ---")
    newsletter_pm = generate_newsletter_pm(inputs["topic"], draft)
    print(newsletter_pm)

    # Stage 4: Distribution
    print("Distributing to HubSpot...\n")
    summary = distribute_to_hubspot(
        inputs["topic"], newsletter_head, newsletter_creative, newsletter_pm
    )
    print("--- HubSpot Summary ---")
    print(summary)

    # Stage 5: Reporting
    print("Generating report...\n")
    newsletters = {"head": newsletter_head, "creative": newsletter_creative, "pm": newsletter_pm}
    report = generate_report(inputs["topic"], newsletters)

    print("--- Report: Metrics ---")
    for persona, m in report["metrics"].items():
        print(f"  {persona.upper()}: open={m['open_rate']:.1%}, click={m['click_rate']:.1%}, unsub={m['unsubscribe_rate']:.2%}")
    print("\n--- Report: AI Analysis ---")
    print(report["ai_analysis"])

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    os.makedirs("outputs", exist_ok=True)
    output_path = f"outputs/run_{timestamp}.json"

    with open(output_path, "w") as f:
        json.dump(
            {
                "timestamp": timestamp,
                "topic": inputs["topic"],
                "audience": inputs["audience"],
                "intent": inputs["intent"],
                "outline": outline,
                "draft": draft,
                "newsletters": {
                    "head": newsletter_head,
                    "creative": newsletter_creative,
                    "pm": newsletter_pm,
                },
                "hubspot_summary": summary,
                "report": report,
            },
            f,
            indent=2,
        )

    html_path = generate_html_report(
        inputs["topic"], report, newsletters, summary, timestamp
    )

    print(f"\nRun saved to {output_path}")
    print(f"HTML report saved to {html_path}")


if __name__ == "__main__":
    run_pipeline()
