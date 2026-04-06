import json
from collections import defaultdict

# 1. 원본 JSON 파일 읽기
with open("/data/gangmin3552/project/llavavideo/adjust_hair_merg.json", "r") as f:
    raw_data = [json.loads(line) for line in f]

# 2. video_id별, seg_index별로 모으기
video_dict = defaultdict(dict)
for item in raw_data:
    vid = item["video_id"]
    seg_idx = item["segment_index"]
    captions = item["output"]
    video_dict[vid][seg_idx] = captions

# 3. seg_index 순으로 정렬 후, 캡션 병합
final_dict = {}
for vid, segs in video_dict.items():
    merged_captions = []
    for idx in sorted(segs.keys()):
        # 각 seg_index 내 두 문장을 ". "로 합침
        merged_text = ". ".join(segs[idx])
        merged_captions.append(merged_text)
    final_dict[vid] = merged_captions

# 4. 최종 JSON 저장
with open("adjusthair_gen.json", "w") as f:
    json.dump(final_dict, f, indent=4)
