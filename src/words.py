import re
import urllib.request
from typing import Iterator, Union
from urllib.error import HTTPError


def read_file(filename: str, encoding: str = "ascii") -> Iterator[str]:
    with open(filename, "r", encoding=encoding) as f:
        while (curr := f.readline()) != "":
            yield curr[:-1]


def get_from_dictionary_com() -> None:
    letters = [chr(i) for i in range(97, 123)]
    letters = ["0"] + letters
    with open("../words/unique_words.txt", "w") as f:
        for letter in letters:
            page_num = 1
            while True:
                try:
                    url = urllib.request.urlopen(
                        f"https://www.dictionary.com/list/{letter}/{page_num}"
                    )
                except HTTPError:
                    break
                data = url.read()
                words = re.findall(r'"css-aw8l3w e3scdxh3">([^"<]+)<', str(data))
                for word in words:
                    f.write(f"{word}\n")
                print(f"Done page {page_num} of letter {letter.upper()}")
                page_num += 1


def remove_duplicates() -> None:
    words = set(read_file("../words/old_words.txt"))
    with open("../words/unique_words.txt", "w") as f:
        for word in words:
            f.write(f"{word}\n")


def fix_word(word: str) -> str:
    word = word.replace("&#x27;", "'")
    if word.__contains__(","):
        if len(split := re.split(r"^(\w+), ", word)) > 1 and word.count(",") == 1:
            word = f"{split[2]} {split[1]}"
        if len(split := re.split(r", ([Tt]he)$", word)) > 1:
            word = f"{split[1]} {split[0]}"
    loc = {"word": word}
    if re.match(r"(?:\\x[a-f0-9]{2})+", word):
        error_text = (
            "ERROR"  # If we see this in the output, something's definitely wrong
        )
        loc["word"] = error_text
        exec(f'word = b"{word}".decode(errors="ignore")', globals(), loc)
    assert loc["word"] != "ERROR"
    return loc["word"]


def fix_words() -> None:
    words = read_file("../words/unique_words.txt")
    with open("../words/words.txt", "w", encoding="utf-8") as f:
        for word in map(fix_word, words):
            f.write(f"{word}\n")


def remove_trailing_dash() -> None:
    words = read_file("../words/words.txt", "utf-8")
    out = set()
    for word in words:
        if word.count("-") == len(word):
            continue
        while word[0] == "-":
            word = word[1:]
        while word[-1] == "-":
            word = word[:-1]
        out.add(word)
    with open("../words/words.txt", "w", encoding="utf-8") as f:
        for word in out:
            f.write(f"{word}\n")


if __name__ == "__main__":
    remove_trailing_dash()
