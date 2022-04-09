from dataclasses import dataclass
from typing import List


@dataclass(frozen=True)
class WordData:
    word: str
    data: List[int]
    derivative: List[float]
