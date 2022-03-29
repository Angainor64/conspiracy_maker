import urllib.request
from urllib.error import HTTPError
import re


def get_from_dictionary_com():
    letters = [chr(i) for i in range(97, 123)]
    letters = ['0'] + letters
    print(letters)
    with open('words.txt', 'w') as f:
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
    with open('old_words.txt', 'r') as f:
        words = set(f.read().splitlines())
    with open('words.txt', 'w') as f:
        for word in words:
            f.write(f'{word}\n')


if __name__ == '__main__':
    remove_duplicates()
