from dataclasses import dataclass
from typing import List

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from pytrends.request import TrendReq
from sklearn.linear_model import LinearRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import PolynomialFeatures

timeframe = '2004-01-01 2022-01-01'


@dataclass(frozen=True)
class WordData:
    word: str
    data: List[int]
    derivative: List[float]


def main():
    pytrends = TrendReq(hl='en-US', tz=360)
    # kw_list = ['AJR', 'Of Monsters And Men', 'Geocaching']
    kw_list = ['AJR']
    for kw in kw_list:
        print(kw)
        pytrends.build_payload([kw], timeframe=timeframe)
        result = pytrends.interest_over_time().reset_index()
        if 'results' not in locals():
            results: pd.DataFrame = result
        else:
            results = pd.merge(results, result, on='date')
    # results.plot(x='date', y=kw_list)

    print(results[kw_list[0]].values.tolist())
    # print(np.asarray(results))
    nparray_results = np.asarray(results)
    x = np.arange(nparray_results.shape[0]).reshape(-1, 1)
    y = nparray_results[:, 1].reshape(-1, 1)
    plt.plot(x, y)
    steps = [('polynomial', PolynomialFeatures(degree=10)), ('modal', LinearRegression())]
    pipe = Pipeline(steps)
    pipe.fit(x, y)
    poly_pred = pipe.predict(x)
    sorted_zip = sorted(zip(x, poly_pred))
    x_poly, poly_pred = zip(*sorted_zip)
    plt.plot(x_poly, poly_pred)
    plt.show()


if __name__ == '__main__':
    main()
