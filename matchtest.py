import requests
from bs4 import BeautifulSoup
import difflib
import re

url = "http://www.badminton-a.com/2025circuit/20250524_result_t_01_s.htm"


def fetch_players_from_url(url):
    res = requests.get(url)
    res.encoding = "cp932"
    soup = BeautifulSoup(res.text, "html.parser")

    all_text = soup.get_text()
    # print(all_text)
    # print(soup)
    # ひらがな・カタカナ・漢字のみ、2文字以上の連続文字列を選手名候補として抽出
    candidates = list(set(re.findall(r'[ぁ-んァ-ン一-龥]{2,}', all_text)))
    print(candidates)
    return soup


if __name__ == "__main__":
    fetch_players_from_url(url)
