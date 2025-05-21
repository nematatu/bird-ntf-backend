import requests
from bs4 import BeautifulSoup


def fetch_match_players(url):
    res = requests.get(url)
    res.encoding = "cp932"
    soup = BeautifulSoup(res.text, "html.parser")

    match_players = []
    for tr in soup.find_all("tr", bgcolor="#ddddff"):
        tds = tr.find_all("td")
        if len(tds) >= 8:
            name_pair = f"{tds[3].get_text(strip=True)}{tds[7].get_text(strip=True)}"
            cleaned = name_pair.replace("・", "").replace(" ", "")
            match_players.append(cleaned)
    return match_players
