import csv
import os
from datetime import datetime


def generate_report(log_filepath="data/sms_log.csv", report_dir="reports", skip_reasons=None):
    # read all rows from the sms log
    rows = []
    with open(log_filepath, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(row)

    # reverse so latest records appear at top
    rows = rows[::-1]

    total = len(rows)
    sent   = [r for r in rows if r["status"] == "sent"]
    failed = [r for r in rows if r["status"] == "failed"]

    # build skip reasons HTML block
    skip_html = ""
    if skip_reasons:
        total_skipped = sum(skip_reasons.values())
        if total_skipped > 0:
            skip_html = f"<p class='skipped'>Skipped: {total_skipped}</p><ul>"
            for reason, count in skip_reasons.items():
                if count > 0:
                    skip_html += f"<li>{reason.replace('_', ' ').title()}: {count}</li>"
            skip_html += "</ul>"

    os.makedirs(report_dir, exist_ok=True)
    report_path = os.path.join(report_dir, "report.html")

    html = f"""<!DOCTYPE html>
<html>
<head>
    <title>SMS Report</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 40px; color: #333; }}
        h1 {{ color: #2c3e50; }}
        .summary {{ margin: 20px 0; }}
        .summary p {{ font-size: 16px; margin: 6px 0; }}
        .summary ul {{ margin: 4px 0 10px 20px; font-size: 15px; color: #e67e22; }}
        table {{ border-collapse: collapse; width: 100%; margin-top: 20px; }}
        th {{ background-color: #2c3e50; color: white; padding: 10px; text-align: left; }}
        td {{ padding: 9px 10px; border-bottom: 1px solid #ddd; }}
        tr:hover {{ background-color: #f5f5f5; }}
        .sent {{ color: green; }}
        .failed {{ color: red; }}
        .skipped {{ color: #e67e22; margin: 6px 0; }}
    </style>
</head>
<body>
    <h1>Bulk SMS Report</h1>
    <p>Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>

    <div class="summary">
        <p>Total processed: {total}</p>
        <p class="sent">Sent: {len(sent)}</p>
        <p class="failed">Failed: {len(failed)}</p>
        {skip_html}
    </div>

    <table>
        <tr>
            <th>Name</th>
            <th>Phone</th>
            <th>Message</th>
            <th>Status</th>
            <th>Timestamp</th>
        </tr>
"""

    for row in rows:
        status_class = "sent" if row["status"] == "sent" else "failed"
        html += f"""        <tr>
            <td>{row['name']}</td>
            <td>{row['phone']}</td>
            <td>{row['message']}</td>
            <td class="{status_class}">{row['status']}</td>
            <td>{row['timestamp']}</td>
        </tr>
"""

    html += """    </table>
</body>
</html>"""

    with open(report_path, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"Report saved to: {report_path}")
    return report_path