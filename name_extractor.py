import re


def extract_names_from_text(ocr_text):
    lines = ocr_text.splitlines()
    names = []
    for line in lines:
        parts = re.findall(r'[ぁ-んァ-ン一-龥]{2,}', line)
        names.extend(parts)
    return names


def concat_names(names):
    return ''.join(names)
