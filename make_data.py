from dataclasses import dataclass
from pickle import dump, load
from typing import List, Iterator


@dataclass(frozen=True)
class WordData:
    word: str
    data: List[int]
    derivative: List[float]


def dump_all(data: List[WordData], filename: str) -> None:
    with open(filename, 'wb') as f:
        for value in data:
            dump(value, f)


def load_all(filename: str) -> Iterator[WordData]:
    with open(filename, 'rb') as f:
        while True:
            try:
                yield load(f)
            except EOFError:
                break


loader = load_all('file.dat')

