import json
import os

json_path = "Finturbo - Earnings2Insights Submission.json"


output_dir = os.mkdir("finturbo_output/")

with open(json_path, 'r', encoding='utf-8') as f:
    data = json.load(f)


for i in range(len(data)):
    report_name = data[i]["ECC"]
    report = data[i]["Report"]

    with open(f"finturbo_output/{report_name}.html", 'w', encoding='utf-8') as f:
        f.write(report)
        f.close()