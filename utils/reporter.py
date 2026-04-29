import csv
import os
from datetime import datetime


def generate_report(log_filepath="data/sms_log.csv", report_dir="reports"):
    # read all rows from the sms log
    rows = []
    with open(log_filepath, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(row)
            # reverse so latest records appear at top
            rows = rows[::-1]

    # count total sent and failed from log
    total = len(rows)
    sent = [r for r in rows if r["status"] == "sent"]
    failed = [r for r in rows if r["status"] == "failed"]

    # create reports folder if it does not exist
    os.makedirs(report_dir, exist_ok=True)

    # always overwrite the same file instead of creating new ones
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
        table {{ border-collapse: collapse; width: 100%; margin-top: 20px; }}
        th {{ background-color: #2c3e50; color: white; padding: 10px; text-align: left; }}
        td {{ padding: 9px 10px; border-bottom: 1px solid #ddd; }}
        tr:hover {{ background-color: #f5f5f5; }}
        .sent {{ color: green; }}
        .failed {{ color: red; }}
    </style>
</head>
<body>
    <h1>Bulk SMS Report</h1>
    <p>Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>

    <div class="summary">
        <p>Total: {total}</p>
        <p class="sent">Sent: {len(sent)}</p>
        <p class="failed">Failed: {len(failed)}</p>
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

    # build one table row per sms log entry
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


    # write mode overwrites the file completely each time
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"Report saved to: {report_path}")
    return report_path