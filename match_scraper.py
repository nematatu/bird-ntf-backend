import requests
from bs4 import BeautifulSoup
import re


def fetch_match_players(url):
    res = requests.get(url)
    res.encoding = "cp932"
    soup = BeautifulSoup(res.text, "html.parser")

    match_players = []
    match_players_opt_ocr = []
    for tr in soup.find_all("tr", bgcolor="#ffffff"):
        tds = tr.find_all("td")
        if len(tds) >= 8:
            name_pair = f"{tds[3].get_text(strip=True)}/{tds[7].get_text(strip=True)}"
            no_slash = name_pair.replace("/", "")
            no_dot = no_slash.replace("・", "")
            cleaned = re.sub(r'\s+', '', no_dot)

            match_players.append(name_pair)
            match_players_opt_ocr.append(cleaned)
    print(match_players_opt_ocr)
    return match_players_opt_ocr, match_players
