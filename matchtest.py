import requests
from bs4 import BeautifulSoup
import difflib

url = "http://www.badminton-a.com/2025circuit/20250524_result_t_01_s.htm"
match_players = []

ocr_names = [
    "川島直水津優表ントン", "石川心菜中出すみれ中津魢互"
]


def fetch_players_from_url(url):
    res = requests.get(url)
    res.encoding = "cp932"
    soup = BeautifulSoup(res.text, "html.parser")

    # all_text = soup.get_text()
    # print(all_text)
    trs = soup.find_all(
        "tr", attrs={"bgcolor": "#ddddff"})
    for tr in trs:
        tds = tr.find_all("td")
        data = [td.get_text(strip=True) for td in tds]

        matchplayer = f"{data[3]}{data[7]}"
        delete_blank = matchplayer.strip().split(" ")
        blank_sequence_pair = "".join(delete_blank)

        delete_dot = blank_sequence_pair.strip().split("・")
        dot_sequence_pair = "".join(delete_dot)
        match_players.append(dot_sequence_pair)

    print("match_pairs", match_players)


def find_similar_names(ocr_text, threshold=0.25):
    matched = []
    for name in match_players:
        ratio = difflib.SequenceMatcher(None, ocr_text, name).ratio()
        if ratio >= threshold:
            matched.append((name, ratio))
    return sorted(matched, key=lambda x: x[1], reverse=True)


if __name__ == "__main__":
    fetch_players_from_url(url)
for ocr in ocr_names:
    print(f"OCR名候補: {ocr}")
    matches = find_similar_names(ocr)
    for name, score in matches:
        print(f"  → 類似: {name} (score: {score:.2f})")
    print()
