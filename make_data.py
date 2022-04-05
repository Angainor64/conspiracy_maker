from pickle import dump, load
from time import sleep, strftime
from typing import List, Iterator, Iterable

from pytrends.exceptions import ResponseError
from pytrends.request import TrendReq
from requests.exceptions import RequestException

from main import WordData
from words import read_file


timeframe = '2004-01-01 2022-01-01'


class MaxRetriesExceeded(RuntimeError):
    def __init__(self):
        super().__init__()


def dump_all(filename: str, data: Iterable[WordData], mode: str = 'a') -> None:
    with open(filename, f'{mode}b') as f:
        for thing in data:
            dump(thing, f)


def load_all(filename: str) -> Iterator[WordData]:
    with open(filename, 'rb') as f:
        while True:
            try:
                yield load(f)
            except EOFError:
                break


def get_trend(word: str, req: TrendReq) -> List[int]:
    req.build_payload([word], timeframe=timeframe)
    return req.interest_over_time().reset_index()[word].values.tolist()


def get_derivative(data: List[int]) -> List[float]:
    out: List[float] = []
    for i in range(1, len(data) - 1):
        y1, y2 = data[i - 1], data[i + 1]
        x1, x2 = i - 1, i + 1
        out.append((y2 - y1) / (x2 - x1))
    return out


def get_all_word_data(words: Iterator[str], last_done: str = None) -> Iterator[WordData]:
    found_start = last_done is None
    req = TrendReq(hl='en-US', tz=360)
    for word in words:
        if not found_start:
            if word == last_done:
                found_start = True
                word = words.__next__()
            continue
        while True:
            try:
                print(f'Attempting to build payload for {word}...', end='')
                req.build_payload([word], timeframe=timeframe)
                print('Done.')
                break
            except ResponseError as e:
                print('\nResponse error. Waiting 60 secs...')
                sleep(60)
        while True:
            try:
                print(f'Attempting to get interest over time for {word}...', end='')
                result = req.interest_over_time().reset_index()
                print('Done.')
                break
            except ResponseError as e:
                print('\nResponse error. Waiting 60 secs...')
                sleep(60)
        if result.empty:
            continue
        data = result[word].values.tolist()
        derivative = get_derivative(data)
        yield WordData(word, data, derivative)


def get_remaining_word_data() -> None:
    last = ''
    words = read_file('words.txt', 'utf-8')
    try:
        for word_data in load_all('word_data.dat'):
            last = word_data.word
        dump_all('word_data.dat', get_all_word_data(words, last))
    except FileNotFoundError:
        dump_all('word_data.dat', get_all_word_data(words))


if __name__ == '__main__':
    # all_words = read_file('words.txt', 'utf-8')
    # print(set(map(lambda a: a[0], all_words)))
    while True:
        try:
            get_remaining_word_data()
        except RequestException as e:
            print(str(e))
            print(strftime('%H:%M'))
