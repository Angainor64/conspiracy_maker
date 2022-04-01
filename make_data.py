from dataclasses import dataclass
from pickle import dump, load
from typing import List, Iterator, Iterable
from pytrends.request import TrendReq
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import Pipeline
import numpy as np
from main import timeframe


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


# def get_trends(word: str, req: TrendReq) -> :



loader = load_all('file.dat')
