import os
import subprocess

# --- 설정 ---
url = "https://www.youtube.com/watch?v=a_Q6uef63Lc"
output_dir = "/local_datasets/SSBDexam/"
cookie_file_path = "/data/gangmin3552/project/llavavideo/cookies.txt"  # 필요 없으면 제거 가능

os.makedirs(output_dir, exist_ok=True)
output_template = os.path.join(output_dir, "%(title)s.%(ext)s")

# --- 다운로드 ---
try:
    download_cmd = [
        "yt-dlp",
        url,
        "-o", output_template,
        "--cookies", cookie_file_path
    ]
    print(f"📥 Downloading video from {url} ...")
    subprocess.run(download_cmd, check=True)
    print("✅ Download complete!")

except subprocess.CalledProcessError as e:
    print("❌ Download failed:", e)
