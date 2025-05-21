from vision_client import run_vision_ocr
from image_utils import get_video_url, take_screenshot, crop_image
from name_extractor import extract_names_from_text, concat_names
from match_scraper import fetch_match_players
from matcher import find_similar_names

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
    },
]

url = "http://www.badminton-a.com/2025circuit/20250524_result_t_01_s.htm"
match_players = fetch_match_players(url)

for channel in channels:
    name = channel["name"]
    print(f"\n==== チャンネル{name} ====")

    video_url = get_video_url(channel["url"])
    image_path = f"images/screenshot_{name}.png"
    cropped_path = f"images/cropped_{name}.png"

    take_screenshot(video_url, image_path)
    crop_image(image_path, channel["crop_box"], cropped_path)

    text = run_vision_ocr(cropped_path)
    names = extract_names_from_text(text)
    concat_name = concat_names(names)

    print("合結果:", concat_name)
    print("類似結果:")
    for match, score in find_similar_names(match_players, concat_name):
        print(f"  → {match} (score: {score:.2f})")
