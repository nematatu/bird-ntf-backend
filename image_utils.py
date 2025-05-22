from PIL import Image
import subprocess
from io import BytesIO
import os

video_url_cache = {}


CACHE_FILE = "urls.txt"

# キャッシュを辞書として読み込む


def load_url_cache():
    cache = {}
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, "r", encoding="utf-8") as f:
            for line in f:
                if "," in line:
                    url, stream_url = line.strip().split(",", 1)
                    cache[url] = stream_url
    return cache

# キャッシュに追記保存


def save_url_cache(cache):
    with open(CACHE_FILE, "w", encoding="utf-8") as f:
        for url, stream_url in cache.items():
            f.write(f"{url},{stream_url}\n")

# URL取得関数


def get_video_url(youtube_url):
    print("check cache for URL...")
    cache = load_url_cache()
    if youtube_url in cache:
        print("URL from cache.")
        return cache[youtube_url]

    print("fetching video URL via yt-dlp...")
    result = subprocess.run(
        ["yt-dlp", "-f", "bestvideo[height<=1080]", "-g", youtube_url],
        capture_output=True, text=True, check=True
    )
    stream_url = result.stdout.strip()

    # キャッシュに保存
    cache[youtube_url] = stream_url
    save_url_cache(cache)

    return stream_url


def take_screenshot(video_url):
    print("take screenshot...")
    process = subprocess.run(
        ["ffmpeg", "-y", "-loglevel", "quiet", "-i", video_url,
         "-frames:v", "1", "-f", "image2pipe", "-vcodec", "png", "-"],
        capture_output=True, check=True
    )
    return Image.open(BytesIO(process.stdout))


def crop_image(pil_image, crop_box):
    return pil_image.crop(crop_box)
