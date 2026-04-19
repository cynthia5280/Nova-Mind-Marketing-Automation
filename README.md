# NovaMind Marketing Automation Pipeline

## Overview

NovaMind is a fictional AI-powered workflow automation tool built for social media agencies. This pipeline demonstrates how NovaMind's value proposition — eliminating repetitive, manual work — can itself be proven through automation.

The pipeline takes a single blog topic and fully automates the journey from content brief to CRM-logged campaign: generating a structured outline, writing a full blog draft, segmenting it into three persona-targeted newsletters, distributing contact records and campaign notes to HubSpot, and producing a performance report with AI-generated analysis.

---

## Architecture

The pipeline runs across five sequential stages, each feeding its output into the next:

**Stage 2 — Generation** (`stage_2_generation/`)
`outline_agent.py` takes the topic, audience, and intent and generates a 5-section blog outline. `writer_agent.py` takes that outline and writes a 400–600 word blog draft. Both use Claude Haiku via the Anthropic SDK.

**Stage 3 — Segmentation** (`stage_3_segmentation/`)
`newsletter_agent.py` takes the blog draft and generates three distinct 150–200 word newsletter versions — one per persona. Each is written from a different angle using a persona-specific system prompt.

**Stage 4 — Distribution** (`stage_4_distribution/`)
`hubspot_agent.py` creates three mock contacts in HubSpot (one per persona), tags each with a persona property, and logs a campaign note containing the newsletter content and send date. Uses the HubSpot CRM API directly via `requests`.

**Stage 5 — Reporting** (`stage_5_reporting/`)
`report_agent.py` simulates realistic open, click, and unsubscribe metrics per persona, then calls Claude Haiku to generate a brief AI analysis comparing performance and recommending next steps. `html_report.py` renders a branded HTML report with metric cards, a Chart.js bar chart, AI analysis, and HubSpot contact summary.

**Outputs**
Every run saves a `outputs/run_{timestamp}.json` with all pipeline data and a `outputs/report_{timestamp}.html` visual report.

---

## Personas

Three personas were chosen to reflect the full decision-making unit inside a social media agency — the people who would actually evaluate, advocate for, or block a tool like NovaMind:

**Head of Agency** — Owns P&L. Managing 50–200 clients means headcount pressure is constant. They're evaluating NovaMind as a cost-avoidance play: can it replace a hire? The messaging leads with ROI, margin, and scale.

**Creative (Designer / Copywriter)** — Doesn't care about business metrics. They're drowning in repetitive change requests — same asset, different caption, 80 times over — and losing the creative energy that made them good at their job. The messaging speaks to reclaiming creative focus.

**Project Manager** — Lives in Slack, email, and spreadsheets juggling approvals, deadlines, and deliverables across every client simultaneously. They need a system that acts like a team member, not another tool to manage. The messaging speaks to chaos reduction and reliability.

Together these three cover the buyer (Head), the end user most likely to champion adoption (Creative), and the operational owner who determines whether the tool actually gets used (PM).

---

## Tools and Models Used

| Component | Tool / Model |
|---|---|
| Content generation (outline, draft, newsletters, report) | Anthropic Claude Haiku (`claude-haiku-4-5-20251001`) via `anthropic` Python SDK |
| Legacy / fallback generation | Google Gemini (`gemini-2.5-flash-lite`) via `google-genai` SDK |
| CRM distribution | HubSpot CRM API v3 via `requests` |
| Environment management | `python-dotenv` |
| HTML report chart | Chart.js (CDN) |
| Language | Python 3.10+ |

---

## Assumptions

- **Mock contacts**: The three HubSpot contacts (Rachel Monroe, Jordan Voss, Marcus Chen) are fictional. No real people are contacted.
- **Simulated metrics**: Open rates (25–45%), click rates (3–8%), and unsubscribe rates (0.1–0.5%) are randomly generated within realistic industry ranges. No emails are actually sent.
- **No email delivery**: The pipeline logs campaign notes to HubSpot but does not send newsletters via any email service provider.
- **Single run per execution**: Each `python main.py` run is independent. There is no deduplication of contacts across runs beyond HubSpot's built-in 409 conflict handling (which fetches the existing contact by email).
- **HubSpot persona property**: The `hs_persona` property must exist in your HubSpot portal. If it does not, contact creation will succeed but the persona tag will be silently ignored.

---

## Setup

```bash
# 1. Clone the repo
git clone <repo-url>
cd mkt-automation

# 2. Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment variables
cp .env.example .env
# Open .env and add your keys:
#   ANTHROPIC_API_KEY=...
#   HUBSPOT_ACCESS_TOKEN=...

# 5. Run the pipeline
python main.py
```

When prompted, enter a blog topic, target audience description, and content intent. The pipeline runs all five stages automatically.

---

## Output

After each run, two files are saved to `outputs/`:

- **`outputs/run_{timestamp}.json`** — Full pipeline data including inputs, outline, draft, all three newsletters, HubSpot summary, and performance report with AI analysis.
- **`outputs/report_{timestamp}.html`** — Visual HTML report with a NovaMind-branded header, per-persona metric cards (color-coded against average), a click rate bar chart, AI analysis, and HubSpot contact log. Open directly in any browser.
