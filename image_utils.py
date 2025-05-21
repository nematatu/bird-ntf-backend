from PIL import Image
import subprocess
import sys


def get_video_url(youtube_url):
    print("take url...")
    result = subprocess.run(["yt-dlp", "-f", "bestvideo[height<=1080]", "-g", youtube_url],
                            capture_output=True, text=True, check=True)
    return result.stdout.strip()


def take_screenshot(video_url, output_path):
    print("take screenshot...")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "quiet", "-i", video_url,
                    "-frames:v", "1", "-q:v", "2", output_path],
                   check=True)


def crop_image(image_path, crop_box, output_path):
    with Image.open(image_path) as img:
        cropped = img.crop(crop_box)
        cropped.save(output_path)
