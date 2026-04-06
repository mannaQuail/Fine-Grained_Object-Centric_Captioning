import os
import subprocess

def split_video(video_path, chunk_length=1):
    # 원본 디렉토리와 파일명 분리
    base_dir = os.path.dirname(video_path)
    filename = os.path.basename(video_path)
    name, ext = os.path.splitext(filename)

    # 저장할 폴더 생성
    output_dir = os.path.join(base_dir, f"{name}_chunks")
    os.makedirs(output_dir, exist_ok=True)

    # 출력 파일명 패턴
    output_pattern = os.path.join(output_dir, f"{name}_%03d{ext}")

    # ffmpeg 명령어 (3초 단위로 쪼개기)
    cmd = [
        "ffmpeg",
        "-i", video_path,
        "-c", "copy",       # 인코딩 없이 그대로 복사 (빠름)
        "-map", "0",
        "-f", "segment",
        "-segment_time", str(chunk_length),
        output_pattern
    ]

    subprocess.run(cmd, check=True)
    print(f"✅ 쪼개진 영상이 {output_dir} 에 저장되었습니다.")

# 사용 예시
split_video("/data/gangmin3552/project/llavavideo/intent_video (3)/5441845281.mp4")
