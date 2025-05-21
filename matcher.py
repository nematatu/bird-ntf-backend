import difflib


def find_similar_names(match_players, ocr_text, threshold=0.25):
    matched = []
    for name in match_players:
        ratio = difflib.SequenceMatcher(None, ocr_text, name).ratio()
        if ratio >= threshold:
            matched.append((name, ratio))
    return sorted(matched, key=lambda x: x[1], reverse=True)
