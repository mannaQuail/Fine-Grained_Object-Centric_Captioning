import json
from collections import defaultdict

# 원본 JSONL 파일 읽기
with open("/data/gangmin3552/project/llavavideo/cap3_adjusthair_20250824_225557.json", "r", encoding="utf-8") as f:
    data = [json.loads(line) for line in f]

# segment_index 기준으로 output 모으기
grouped = defaultdict(list)
meta = {}

for item in data:
    idx = item["segment_index"]
    grouped[idx].extend(item["output"])   # output 합치기
    
    # question은 빼고 저장
    meta[idx] = {k: v for k, v in item.items() if k not in ["output", "question"]}

# segment_index 순서대로 저장
results = []
for idx in sorted(grouped.keys()):
    entry = meta[idx].copy()
    entry["output"] = grouped[idx]
    results.append(entry)

# JSONL 파일로 저장
with open("adjust_hair_merg.json", "w", encoding="utf-8") as f:
    for item in results:
        f.write(json.dumps(item, ensure_ascii=False) + "\n")