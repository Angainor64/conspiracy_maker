from pytrends.request import TrendReq
import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import Pipeline
import numpy as np


def main():
    pytrends = TrendReq(hl='en-US', tz=360)
    # kw_list = ['AJR', 'Of Monsters And Men', 'Geocaching']
    kw_list = ['AJR']
    for kw in kw_list:
        print(kw)
        pytrends.build_payload([kw])
        result = pytrends.interest_over_time().reset_index()
        if 'results' not in locals():
            results = result
        else:
            results = pd.merge(results, result, on='date')
    # results.plot(x='date', y=kw_list)

    # print(results)
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
