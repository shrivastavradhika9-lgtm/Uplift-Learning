import json
from pathlib import Path
from datetime import datetime

LOG_FILE = Path("results/audit_log.jsonl")
OUTPUT_FILE = Path("results/monitoring_report.txt")


def load_predictions():
    records = []

    if not LOG_FILE.exists():
        return records

    with open(LOG_FILE, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                records.append(json.loads(line))

    return records


def main():
    records = load_predictions()

    if not records:
        print("No prediction records found.")
        return

    uplifts = [r["estimated_uplift"] for r in records]

    total_predictions = len(records)
    avg_uplift = sum(uplifts) / total_predictions
    min_uplift = min(uplifts)
    max_uplift = max(uplifts)

    recommendations = [
        r["recommendation"]
        for r in records
    ]

    recommended = recommendations.count("Recommend Intervention")
    not_recommended = recommendations.count("No Intervention")
    recommendation_rate = (recommended / total_predictions) * 100

    report = f"""
MDS-02 UPLIFT MODELING PLATFORM
Prediction Monitoring Report
Generated: {datetime.now().isoformat()}

Total Predictions: {total_predictions}

Average Estimated Uplift: {avg_uplift:.4f}
Minimum Estimated Uplift: {min_uplift:.4f}
Maximum Estimated Uplift: {max_uplift:.4f}

Recommend Intervention: {recommended}
No Intervention: {not_recommended}
Recommendation Rate: {recommendation_rate:.2f}%
"""

    OUTPUT_FILE.parent.mkdir(exist_ok=True)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(report)

    print(report)
    print(f"Monitoring report saved to: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()