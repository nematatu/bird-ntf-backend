from vision_client import run_vision_ocr
from image_utils import get_video_url, take_screenshot, crop_image
from name_extractor import extract_names_from_text, concat_names
from match_scraper import fetch_match_players
from matcher import find_similar_names
from flask import Flask, jsonify

app = Flask(__name__)

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


def process_matches():
    # 1) 試合表をスクレイピング
    match_players_opt_ocr, match_players = fetch_match_players(url)

    results = []
    for ch in channels:
        # 2) 動画URL → screenshot → crop
        stream = get_video_url(ch["url"])
        shot = take_screenshot(stream)
        crop = crop_image(shot, ch["crop_box"])

        # 3) OCR → 名前抽出 → 連結
        text = run_vision_ocr(crop)
        names = extract_names_from_text(text)
        concat_name = concat_names(names)

        # 4) 類似度マッチング
        match = find_similar_names(
            match_players_opt_ocr, match_players, concat_name)
        if match:
            matched_name, score = match
        else:
            matched_name, score = None, None

        # 5) レスポンス用にまとめる
        results.append({
            "channel": ch["name"],
            "ocr": concat_name,
            "matched": matched_name,
            "score": score
        })
    return results


@app.route("/results", methods=["GET"])
def get_results():
    data = process_matches()
    return jsonify(data)


if __name__ == "__main__":
    app.run(port=5000)
