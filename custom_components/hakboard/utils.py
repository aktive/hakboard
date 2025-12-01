def parse_text_into_ids(text: str):
    ids = set()
    if not text:
        return ids

    text = text.replace(" ", "")

    for part in text.split(","):
        if "-" in part:
            start, end = part.split("-")
            ids.update(range(int(start), int(end) + 1))
        else:
            ids.add(int(part))

    return ids
