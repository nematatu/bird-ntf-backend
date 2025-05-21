import subprocess
import sys
import pytesseract
from PIL import Image

# stream_url = "https://www.youtube.com/watch?v=-P7KpJwcRtM"
stream_url = "https://www.youtube.com/watch?v=4QWaV1DuC7Q"
output_image = "screenshot.png"


def get_video_url(youtube_url):
    try:
        result = subprocess.run(
            ["yt-dlp", "-f", "best", "-g", youtube_url],
            capture_output=True,
            text=True,
            check=True
        )
        print(result)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print("failed", e.stderr)
        sys.exit(1)


def take_screenshot(youtube_url):
    try:
        cmd = ["ffmpeg", "-y", "-i", youtube_url,
               "-frames:v", "1", "-q:v", "2", output_image]
        subprocess.run(cmd, stdout=subprocess.DEVNULL)

    except subprocess.CalledProcessError as e:
        print("failed scr", e.stderr)
        sys.exit(1)


def run_ocr():
    img = Image.open(output_image)
    text = pytesseract.image_to_string(img)
    return text


if __name__ == "__main__":
    print("taking url...")
    url = get_video_url(stream_url)

    print("taking scr..")
    take_screenshot(url)

    print("run ocr...")
    text = run_ocr()
    print(text)
