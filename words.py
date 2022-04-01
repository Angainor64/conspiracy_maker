import re
import urllib.request
from typing import Iterator, Union
from urllib.error import HTTPError


# TODO: Things to fix from unique_words.txt:
# things that end in ', the'
#   ', the
# Lincoln, Abraham
#   Single word, comma space '\w+, '


def read_file(filename: str) -> Iterator[Union[str, bytes]]:
    with open(filename, 'r') as f:
        curr = ' '
        while (curr := f.readline()) != '':
            yield curr[:-1]


def get_from_dictionary_com():
    letters = [chr(i) for i in range(97, 123)]
    letters = ['0'] + letters
    print(letters)
    with open('unique_words.txt', 'w') as f:
        for letter in letters:
            page_num = 1
            while True:
                try:
                    url = urllib.request.urlopen(f'https://www.dictionary.com/list/{letter}/{page_num}')
                except HTTPError:
                    break
                data = url.read()
                words = re.findall(r'"css-aw8l3w e3scdxh3">([^"<]+)<', str(data))
                for word in words:
                    f.write(f'{word}\n')
                print(f'Done page {page_num} of letter {letter.upper()}')
                page_num += 1


def remove_duplicates():
    words = set(read_file('old_words.txt'))
    with open('unique_words.txt', 'w') as f:
        for word in words:
            f.write(f'{word}\n')


def fix_word(word: str):
    word = word.replace('&#x27;', '\'')
    if word.__contains__(','):
        if len(split := re.split(r'^(\w+), ', word)) > 1 and word.count(',') == 1:
            word = f'{split[2]} {split[1]}'
        if len(split := re.split(r', ([Tt]he)$', word)) > 1:
            word = f'{split[1]} {split[0]}'
    loc = {'word': word}
    if re.match(r'(?:\\x[a-f0-9]{2})+', word):
        error_text = 'ERRORERRORERRORERRORERRORERRORERRORERRORERRORERRORERRORERRORERRORERRORERROR'
        loc['word'] = error_text
        print(word)
        exec(f'word = b"{word}".decode(errors="ignore")', globals(), loc)
        print(loc['word'], '\n')
    return loc['word']


def fix_words():
    words = read_file('unique_words.txt')
    with open('words.txt', 'w', encoding='utf-8') as f:
        for word in map(fix_word, words):
            f.write(f'{word}\n')


if __name__ == '__main__':
    fix_words()
    # with open('unique_words.txt', 'r') as f:
    #     words = f.read().splitlines()
    #     exec(f'print(b"{words[434]}".decode("utf-8"))')
