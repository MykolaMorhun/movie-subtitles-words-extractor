
from collections import Counter
import re

# 00:01:04,189 --> 00:01:06,816
SUBTITLE_TIME_PATTERN = re.compile(r"^\d\d:\d\d:\d\d,\d\d\d --> \d\d:\d\d:\d\d,\d\d\d$")
TAG_PATTERN = re.compile(r"<\S+?>")
SPLIT_WORD_PATTERN = re.compile(r"[ \t\n\r.,;:!?\(\)\[\]{}<>\\/\"_=&]+")
A_WORD_PATTERN = re.compile("[a-zA-Z]{2}")
STRIP_WORD_CHARS = r"'+-—#$%~*@^1234567890’”“`…"

def create_words_counter(text: str, is_subtitles: bool = True) -> Counter[str]:
    """
    Takes a subtitles (or just text) file content and extracts unique words from it.
    Counts how many times each word occurs.
    """

    words_counter: Counter[str] = Counter()

    lines: list[str] = text.splitlines()
    for line in lines:
        if line == "":
            continue
        if is_subtitles:
            # skip subtitle phrase number lines
            if line.isnumeric():
                continue
            # skip timestamps line
            if SUBTITLE_TIME_PATTERN.match(line):
                continue
        line = re.sub(TAG_PATTERN, '', line)

        words = SPLIT_WORD_PATTERN.split(line)
        for word in words:
            if not A_WORD_PATTERN.search(word):
                # If string doesn't have two letters in a row, doesn't consider it a word.
                continue
            w = word.lower()
            w = w.strip(STRIP_WORD_CHARS)

            # English-specific cases:
            # Handle possesive case
            if w.endswith("'s"):
                w = w[:-2]
            # Check for n-th
            if w == "th":
                continue

            words_counter[w] += 1

    del words_counter[""]

    return words_counter
