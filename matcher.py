import difflib


def find_similar_names(match_players_opt_ocr, match_players, ocr_text, threshold=0.1):
    matched = []
    for index, name in enumerate(match_players):
        ratio = difflib.SequenceMatcher(None, ocr_text, name).ratio()
        if ratio >= threshold:
            matched.append((match_players[index], ratio))
    matched = sorted(matched, key=lambda x: x[1], reverse=True)
    if matched:
        return matched[0]  # 一番スコアが高いものだけ返す
    else:
        return None
