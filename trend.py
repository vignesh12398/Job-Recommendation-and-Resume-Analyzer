import time
import numpy as np

from pytrends.request import TrendReq
pytrends = TrendReq(hl='en-US', tz=330)
def get_trend(role):

        pytrends.build_payload([role], timeframe='today 12-m')
        data=pytrends.interest_over_time()
        return data

def trend_direction(data,role):
    if data.empty:
        return "No data"
    values = data[role].values

    trend = np.polyfit(range(len(values)), values, 1)[0]
    if trend>0:
        return"📈 Increasing"
    elif trend<0:
        return "📉 Decreasing"
    else:
        return "➖ Stable"