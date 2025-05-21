from google.cloud import vision
from PIL import Image
import io
import subprocess
import sys
import cv2
import re

# stream_url = "https://www.youtube.com/watch?v=-P7KpJwcRtM"
str_url = "https://www.youtube.com/watch?v=Dzk2ErmANXk"
output_image = "screenshot.png"


def get_video_url(youtube_url):
    try:
        result = subprocess.run(["yt-dlp", "-f", "bestvideo[height<=1080]", "-g", youtube_url],
                                capture_output=True,
                                text=True,
                                check=True
                                )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print("failed", e.stderr)
        sys.exit(1)


def take_screenshot(youtube_url):
    try:
        cmd = ["ffmpeg", "-y", "-loglevel", "quiet",   "-i", youtube_url,
               "-frames:v", "1", "-q:v", "2", output_image]
        subprocess.run(cmd, stdout=subprocess.DEVNULL)

    except subprocess.CalledProcessError as e:
        print("failed scr", e.stderr)
        sys.exit(1)


crop_box = (310, 100, 580, 280)


def crop_image(image_path):
    with Image.open(image_path) as img:
        cropped_img = img.crop(crop_box)
    cropped_img.save("cropped_image.png")


def extract_name_boxes(image_path):
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 180, 255, cv2.THRESH_BINARY)

    contours, _ = cv2.findContours(
        thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    boxes = []
    for i, cnt in enumerate(contours):
        x, y, w, h = cv2.boundingRect(cnt)
        if 200 < w < 800 and 40 < h < 200:
            boxes.append((x, y, x + w, y + h))
    print(boxes)
    return boxes


# Vision APIクライアントの初期化
client = vision.ImageAnnotatorClient()


# def run_vision_ocr_from_box(image_path, crop_box):
#     with Image.open(image_path) as img:
#         # cropped_img = img.crop(crop_box)
#
#         # Vision API用バイナリ作成
#         # img_byte_arr = io.BytesIO()
#         # cropped_img.save(img_byte_arr, format="PNG")
#         # content = img_byte_arr.getvalue()
#
#         img_byte_arr = io.BytesIO()
#         img.save(img_byte_arr, format="PNG")
#         content = img_byte_arr.getvalue()
#     image = vision.Image(content=content)
#     response = client.text_detection(image=image)
#     texts = response.text_annotations
#     if texts:
#         return texts[0].description.strip()
#     return ""


def run_vision_ocr(image_path):
    with Image.open(image_path) as img:
        # cropped_img = img.crop(crop_box)

        # Vision API用バイナリ作成
        # img_byte_arr = io.BytesIO()
        # cropped_img.save(img_byte_arr, format="PNG")
        # content = img_byte_arr.getvalue()

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
    # name_lines = []
    name_candidates = []
    for line in lines:
        # line = line.strip()
        parts = re.findall(r'[ぁ-んァ-ン一-龥]{2,}', line)
        name_candidates.extend(parts)
        # 日本語文字（ひらがな・カタカナ・漢字）と空白（半角・全角）のみを許可
        # if re.fullmatch(r'[ \u3000\u3040-\u30FF\u4E00-\u9FFF]{2,}', line):
        #     name_lines.append(line)
    # return name_lines
    return name_candidates


if __name__ == "__main__":
    print("taking url...")
    url = get_video_url(str_url)

    print("taking screenshot...")
    take_screenshot(url)

    print("taking crop...")
    crop_image(output_image)

    print("extract white box...")
    boxes = extract_name_boxes("cropped_image.png")

    print("OCR処理開始...dayo")
    result = run_vision_ocr("cropped_image.png")
    print("result...", result)
    names = extract_names_from_text(result)
    for name in names:
        print("---", name)
    # for i, box in enumerate(boxes):
    #     result = run_vision_ocr_from_box("cropped_image.png", box)
    #     names = extract_names_from_text(result)
    #     for name in names:
    #         print("---", name)
