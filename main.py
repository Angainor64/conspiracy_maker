from pytrends.request import TrendReq
import matplotlib
import matplotlib.pyplot as plt


def main():
    pytrends = TrendReq(hl='en-US', tz=360)
    kw_list = ['Creality', 'Taylor Swift']
    pytrends.build_payload(kw_list, geo='US')
    results = pytrends.interest_over_time()
    print(results)
    results.reset_index().plot(x='date', y=['Taylor Swift', 'Creality'])
    plt.show()


if __name__ == '__main__':
    main()
