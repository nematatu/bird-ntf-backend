from google.cloud import vision
from PIL import Image
import io
import subprocess
import sys
import re

# チャンネル設定
channels = [
    {
        "name": "A",
        "url": "https://www.youtube.com/watch?v=rfcNKPLhpSs",
        "crop_box": (310, 100, 580, 280)
    },
    {
        "name": "B",
        "url": "https://www.youtube.com/watch?v=Dzk2ErmANXk",  # 例: 他のURL
        "crop_box": (300, 90, 570, 270)
    },
    {
        "name": "C",
        "url": "https://www.youtube.com/watch?v=uXiUI9440zc",
        "crop_box": (320, 110, 590, 290)
    },
    {
        "name": "D",
        "url": "https://www.youtube.com/watch?v=RCGzJmPNWZ4",
        "crop_box": (400, 95, 700, 260)
    }
]

# Vision API
client = vision.ImageAnnotatorClient()


def get_video_url(youtube_url):
    try:
        result = subprocess.run(["yt-dlp", "-f", "bestvideo[height<=1080]", "-g", youtube_url],
                                capture_output=True,
                                text=True,
                                check=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print("failed", e.stderr)
        sys.exit(1)


def take_screenshot(youtube_url, output_path):
    try:
        cmd = ["ffmpeg", "-y", "-loglevel", "quiet", "-i", youtube_url,
               "-frames:v", "1", "-q:v", "2", output_path]
        subprocess.run(cmd, stdout=subprocess.DEVNULL)
    except subprocess.CalledProcessError as e:
        print("failed scr", e.stderr)
        sys.exit(1)


def crop_image(image_path, crop_box, output_path):
    with Image.open(image_path) as img:
        cropped_img = img.crop(crop_box)
    cropped_img.save(output_path)


def run_vision_ocr(image_path):
    with Image.open(image_path) as img:
        img_byte_arr = io.BytesIO()
        img.save(img_byte_arr, format="PNG")
        content = img_byte_arr.getvalue()
    image = vision.Image(content=content)
    response = client.text_detection(image=image)
    texts = response.text_annotations
    if texts:
        return texts[0].description.strip()
    return ""


def extract_names_from_text(ocr_text):
    lines = ocr_text.splitlines()
    name_candidates = []
    for line in lines:
        parts = re.findall(r'[ぁ-んァ-ン一-龥]{2,}', line)
        name_candidates.extend(parts)
    return name_candidates


if __name__ == "__main__":
    for channel in channels:
        name = channel["name"]
        print(f"\n==== チャンネル{name}の処理 ====")
        output_image = f"images/screenshot_{name}.png"
        cropped_image = f"images/cropped_{name}.png"

        print("taking url...")
        video_url = get_video_url(channel["url"])

        print("taking screenshot...")
        take_screenshot(video_url, output_image)

        print("cropping...")
        crop_image(output_image, channel["crop_box"], cropped_image)

        print("OCR処理中...")
        ocr_result = run_vision_ocr(cropped_image)

        print("名前抽出結果:")
        names = extract_names_from_text(ocr_result)
        for n in names:
            print("---", n)
