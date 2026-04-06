import json
from collections import defaultdict
from pathlib import Path

# 1. 처리할 폴더 경로
folder_path = "/data/gangmin3552/project/llavavideo/caption_test/3fps"  # 여기에 JSON 파일들이 있는 폴더 경로

# 2. 폴더 내 모든 JSON 파일 읽기
all_files = list(Path(folder_path).glob("*.json"))

raw_data = []
for file in all_files:
    with open(file, "r") as f:
        # 파일이 한 줄에 한 JSON 객체라면 line별로 읽어서 load
        for line in f:
            raw_data.append(json.loads(line))

# 3. video_id별, seg_index별로 모으기
video_dict = defaultdict(dict)
for item in raw_data:
    vid = item["video_id"]
    seg_idx = item["segment_index"]
    captions = item["output"]
    video_dict[vid][seg_idx] = captions

# 4. seg_index 순으로 정렬 후, 캡션 병합
final_dict = {}
for vid, segs in video_dict.items():
    merged_captions = []
    for idx in sorted(segs.keys()):
        merged_text = ". ".join(segs[idx])  # 각 seg_index 내 문장 병합
        merged_captions.append(merged_text)
    final_dict[vid] = merged_captions

# 5. 최종 JSON 저장
output_file = Path(folder_path) / "merged_all_captions.json"
with open(output_file, "w") as f:
    json.dump(final_dict, f, indent=4)

print(f"모든 JSON 파일이 합쳐져 {output_file}로 저장되었습니다.")
