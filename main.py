from typing import List, Iterable, Tuple, Union

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from pytrends.request import TrendReq
from sklearn.linear_model import LinearRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import PolynomialFeatures

from make_data import get_trend, get_derivative, load_all
from word_data import WordData


timeframe = '2004-01-01 2022-01-01'


def get_word_data(word: str) -> WordData:
    req = TrendReq(hl='en-US', tz=360)
    data = get_trend(word, req)
    derivative = get_derivative(data)
    return WordData(word, data, derivative)


def get_array_difference(array1: List[float], array2: List[float]) -> float:
    return sum([abs(a - b) for a, b in zip(array1, array2)])


def get_word_data_difference(word1: WordData, word2: WordData, weights: Tuple) -> float:
    data_diff = get_array_difference(word1.data, word2.data) * weights[0]
    deriv_diff = get_array_difference(word1.derivative, word2.derivative) * weights[1]
    return data_diff + deriv_diff


def find_min_diff(word: str, weights: Tuple, num_return: int = 1, word_list: Iterable[WordData] = None) \
        -> List[Tuple[str, float]]:
    if num_return < 1:
        raise ValueError('num_return must be greater than 0')
    out: List[Tuple[str, float]] = []
    if word_list is None:
        word_list = load_all('word_data.dat')
    word_data = get_word_data(word)
    i = 1
    for other in word_list:
        i += 1
        diff = get_word_data_difference(word_data, other, weights)
        if len(out) == num_return:
            if diff > out[-1][1]:
                continue
        for i in range(len(out)):
            if diff < out[i][1]:
                out.insert(i, (other.word, diff))
                break
        if len(out) > num_return:
            del out[-1]
        if len(out) == 0:
            out.append((other.word, diff))
        # print(out)
    return out


def display_results(word: str, num_results: int, weights: Tuple):
    pytrends = TrendReq(hl='en-US', tz=360)
    # kw_list = ['AJR', 'Of Monsters And Men', 'Geocaching']
    min_diffs = find_min_diff(word, weights, num_results + 1)
    kw_list = [result[0] for result in min_diffs]
    if word in kw_list:
        kw_list.remove(word)
    kw_list = [word] + kw_list[0:num_results]
    for kw in kw_list:
        print(kw)
        pytrends.build_payload([kw], timeframe=timeframe)
        result = pytrends.interest_over_time().reset_index()
        if 'results' not in locals():
            results: pd.DataFrame = result
        else:
            results = pd.merge(results, result, on='date')
    results.plot(x='date', y=kw_list)
    plt.show()


# def main():
#     print(results[kw_list[0]].values.tolist())
#     print(np.asarray(results))
#     nparray_results = np.asarray(results)
#     x = np.arange(nparray_results.shape[0]).reshape(-1, 1)
#     y = nparray_results[:, 1].reshape(-1, 1)
#     plt.plot(x, y)
#     steps = [('polynomial', PolynomialFeatures(degree=10)), ('modal', LinearRegression())]
#     pipe = Pipeline(steps)
#     pipe.fit(x, y)
#     poly_pred = pipe.predict(x)
#     sorted_zip = sorted(zip(x, poly_pred))
#     x_poly, poly_pred = zip(*sorted_zip)
#     plt.plot(x_poly, poly_pred)
#     plt.show()


if __name__ == '__main__':
    # final = find_min_diff('Ted Cruz', 10)
    # print(f'\nFinal:\n{final}')
    display_results('Putin', 1, (1, 5))
