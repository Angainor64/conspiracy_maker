from dataclasses import dataclass
from pickle import dump, load
from typing import List, Iterator, Iterable


@dataclass(frozen=True)
class WordData:
    word: str
    data: List[int]
    derivative: List[float]


def dump_all(filename: str, data: Iterable[WordData]) -> None:
    with open(filename, 'wb') as f:
        for thing in data:
            dump(thing, f)


def load_all(filename: str) -> Iterator[WordData]:
    with open(filename, 'rb') as f:
        while True:
            try:
                yield load(f)
            except EOFError:
                break


loader = load_all('file.dat')

