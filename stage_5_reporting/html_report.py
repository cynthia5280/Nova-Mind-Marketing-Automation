import os
from datetime import datetime


PERSONA_LABELS = {
    "head": "Head of Agency",
    "creative": "Creative",
    "pm": "Project Manager",
}


def _color(value: float, average: float, lower_is_better: bool = False) -> str:
    above = value >= average
    if lower_is_better:
        above = not above
    return "#22c55e" if above else "#ef4444"


def generate_html_report(
    topic: str,
    report: dict,
    newsletters: dict,
    hubspot_summary: str,
    timestamp: str,
) -> str:
    metrics = report["metrics"]
    ai_analysis = report["ai_analysis"]

    personas = ["head", "creative", "pm"]
    avg_open = sum(metrics[p]["open_rate"] for p in personas) / 3
    avg_click = sum(metrics[p]["click_rate"] for p in personas) / 3
    avg_unsub = sum(metrics[p]["unsubscribe_rate"] for p in personas) / 3

    run_date = datetime.strptime(timestamp, "%Y%m%d_%H%M%S").strftime("%B %d, %Y at %H:%M")

    cards_html = ""
    for p in personas:
        m = metrics[p]
        open_color = _color(m["open_rate"], avg_open)
        click_color = _color(m["click_rate"], avg_click)
        unsub_color = _color(m["unsubscribe_rate"], avg_unsub, lower_is_better=True)
        cards_html += f"""
        <div class="card">
            <h3>{PERSONA_LABELS[p]}</h3>
            <div class="metric">
                <span class="metric-label">Open Rate</span>
                <span class="metric-value" style="color:{open_color}">{m['open_rate']:.1%}</span>
            </div>
            <div class="metric">
                <span class="metric-label">Click Rate</span>
                <span class="metric-value" style="color:{click_color}">{m['click_rate']:.1%}</span>
            </div>
            <div class="metric">
                <span class="metric-label">Unsubscribe Rate</span>
                <span class="metric-value" style="color:{unsub_color}">{m['unsubscribe_rate']:.2%}</span>
            </div>
        </div>"""

    click_rates = [round(metrics[p]["click_rate"] * 100, 2) for p in personas]
    chart_labels = [PERSONA_LABELS[p] for p in personas]
    chart_colors = [
        _color(metrics[p]["click_rate"], avg_click) for p in personas
    ]

    hubspot_lines = "".join(
        f"<li>{line}</li>"
        for line in hubspot_summary.replace("HubSpot Distribution Summary:\n", "").strip().splitlines()
    )

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>NovaMind Campaign Report — {topic}</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        * {{ box-sizing: border-box; margin: 0; padding: 0; }}
        body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; background: #f8fafc; color: #1e293b; }}
        .header {{ background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%); color: white; padding: 40px 48px; }}
        .header .brand {{ font-size: 13px; font-weight: 600; letter-spacing: 2px; text-transform: uppercase; opacity: 0.8; margin-bottom: 8px; }}
        .header h1 {{ font-size: 28px; font-weight: 700; margin-bottom: 6px; }}
        .header .meta {{ font-size: 14px; opacity: 0.75; }}
        .content {{ max-width: 960px; margin: 0 auto; padding: 40px 24px; }}
        .section {{ margin-bottom: 40px; }}
        .section-title {{ font-size: 13px; font-weight: 700; letter-spacing: 1.5px; text-transform: uppercase; color: #64748b; margin-bottom: 16px; }}
        .cards {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 16px; }}
        .card {{ background: white; border-radius: 12px; padding: 24px; box-shadow: 0 1px 3px rgba(0,0,0,0.08); }}
        .card h3 {{ font-size: 15px; font-weight: 600; color: #334155; margin-bottom: 16px; padding-bottom: 12px; border-bottom: 1px solid #f1f5f9; }}
        .metric {{ display: flex; justify-content: space-between; align-items: center; padding: 8px 0; }}
        .metric-label {{ font-size: 13px; color: #64748b; }}
        .metric-value {{ font-size: 18px; font-weight: 700; }}
        .chart-wrapper {{ background: white; border-radius: 12px; padding: 24px; box-shadow: 0 1px 3px rgba(0,0,0,0.08); }}
        .analysis-box {{ background: white; border-radius: 12px; padding: 28px; box-shadow: 0 1px 3px rgba(0,0,0,0.08); line-height: 1.7; font-size: 15px; color: #334155; border-left: 4px solid #6366f1; }}
        .hubspot-box {{ background: white; border-radius: 12px; padding: 24px; box-shadow: 0 1px 3px rgba(0,0,0,0.08); }}
        .hubspot-box ul {{ list-style: none; padding: 0; }}
        .hubspot-box li {{ font-size: 13px; font-family: "SF Mono", "Fira Code", monospace; color: #475569; padding: 8px 12px; background: #f8fafc; border-radius: 6px; margin-bottom: 8px; }}
    </style>
</head>
<body>
    <div class="header">
        <div class="brand">NovaMind &mdash; Campaign Report</div>
        <h1>{topic}</h1>
        <div class="meta">Run on {run_date}</div>
    </div>

    <div class="content">
        <div class="section">
            <div class="section-title">Persona Performance</div>
            <div class="cards">{cards_html}</div>
        </div>

        <div class="section">
            <div class="section-title">Click Rate Comparison</div>
            <div class="chart-wrapper">
                <canvas id="clickChart" height="100"></canvas>
            </div>
        </div>

        <div class="section">
            <div class="section-title">AI Analysis</div>
            <div class="analysis-box">{ai_analysis.replace(chr(10), "<br>")}</div>
        </div>

        <div class="section">
            <div class="section-title">HubSpot Distribution</div>
            <div class="hubspot-box">
                <ul>{hubspot_lines}</ul>
            </div>
        </div>
    </div>

    <script>
        new Chart(document.getElementById("clickChart"), {{
            type: "bar",
            data: {{
                labels: {chart_labels},
                datasets: [{{
                    label: "Click Rate (%)",
                    data: {click_rates},
                    backgroundColor: {chart_colors},
                    borderRadius: 6,
                    borderSkipped: false,
                }}]
            }},
            options: {{
                plugins: {{ legend: {{ display: false }} }},
                scales: {{
                    y: {{
                        beginAtZero: true,
                        ticks: {{ callback: v => v + "%" }},
                        grid: {{ color: "#f1f5f9" }}
                    }},
                    x: {{ grid: {{ display: false }} }}
                }}
            }}
        }});
    </script>
</body>
</html>"""

    os.makedirs("outputs", exist_ok=True)
    output_path = f"outputs/report_{timestamp}.html"
    with open(output_path, "w") as f:
        f.write(html)

    return output_path
