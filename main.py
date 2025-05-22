from vision_client import run_vision_ocr
from image_utils import get_video_url, take_screenshot, crop_image
from name_extractor import extract_names_from_text, concat_names
from match_scraper import fetch_match_players
from matcher import find_similar_names

channels = [
    {
        "name": "A",
        "url": "https://www.youtube.com/watch?v=ecCk2cMjAHo",
        "crop_box": (310, 100, 580, 280)
    },
    {
        "name": "B",
        "url": "https://www.youtube.com/watch?v=Hb8y6foGKn4",  # 例: 他のURL
        "crop_box": (330, 90, 600, 270)
    },
    {
        "name": "C",
        "url": "https://www.youtube.com/watch?v=aGaeQlHmuRs",
        "crop_box": (370, 130, 550, 300)
    },
    {
        "name": "D",
        "url": "https://www.youtube.com/watch?v=qf_NCGg67Jo",
        "crop_box": (400, 95, 700, 260)
    },
]

url = "http://www.badminton-a.com/2025circuit/20250524_result_t_02_s.htm"
match_players_opt_ocr, match_players = fetch_match_players(url)

for channel in channels:
    name = channel["name"]
    print(f"\n==== チャンネル{name} ====")

    video_url = get_video_url(channel["url"])
    screenshot_img = take_screenshot(video_url)
    cropped_img = crop_image(screenshot_img, channel["crop_box"])

    text = run_vision_ocr(cropped_img)
    names = extract_names_from_text(text)
    concat_name = concat_names(names)

    print("OCRの結果:", concat_name)
    print("類似結果:")
    result = find_similar_names(
        match_players_opt_ocr, match_players,  concat_name)

    if result:
        match_name, score = result
        print(match_name)
    else:
        print("No match")
