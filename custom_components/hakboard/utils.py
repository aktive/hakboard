"""Utility functions for HAKboard integration."""


def parse_text_into_ids(text: str) -> set[int]:
    """Parse project filter text into a set of integer IDs.

    Supports formats: "1", "1,5,11", "1-3", "1-3,5,7-9"
    """
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
