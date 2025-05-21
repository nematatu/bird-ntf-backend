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
    trs = soup.find_all(
        "tr", attrs={"bgcolor": "#ffffff"})
    for tr in trs:
        print(tr.get_text(strip=True))
    return soup


if __name__ == "__main__":
    fetch_players_from_url(url)
