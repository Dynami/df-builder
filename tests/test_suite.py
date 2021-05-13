from numpy import sqrt
import pandas as pd

#from ..src.features.features import Feature
from dfbuilder.builder import *
from dfbuilder.features import Feature, Field
import talib

def _labeler(data):
    y = data.y - data.Close
    y[y > 0] = 1
    y[y <= 0] = 0
    return y

data = load_csv_dataframe('./tests/fmib_d.csv', 
            columns=['Open','High','Low','Close','Volume'], 
            index_col='Date')


data = label_data(data, main_column='Close', lookforward=1, custom_labeler=_labeler)


class SMA(Feature):
    def __init__(self, name:str, alias:str=None, period:int=12):
        Feature.__init__(self, name, alias)
        
        self.period = period
    def compute(self, data):

        return talib.SMA(data.Close, self.period)


class AROON(Feature):
    def __init__(self, name:str, alias:str=None, period:int=12):
        Feature.__init__(self, name, alias)
        
        self.period = period
    def compute(self, data):
        return talib.AROON(data.High, data.Low, self.period)


class Decompose(Feature):
    def __init__(self, name:str, alias:str=None, std_period:int=12, trend_period:int=30):
        Feature.__init__(self, name, alias)
        
        self.std_period = std_period
        self.trend_period = trend_period

    def compute(self, data):
        _epsilon = 1e-10
        _sqrt = np.sqrt(252)
        std = talib.STDDEV(data.Close, self.std_period)
        trend = talib.SMA(data.Close, self.trend_period)

        detrend = (data.Close - trend + _epsilon)/(trend + _epsilon)*_sqrt
        std = ((std + _epsilon) / (trend + _epsilon))*_sqrt
        trend = (trend.diff(1)+_epsilon)/(trend+_epsilon)*_sqrt
        
        return trend, detrend, std


data = compute_x_features(data, append=False, features=[
    #Field('Close', 'feat_1'),
    #SMA('Sma', 'feat_2', period=5),
    #SMA('Sma', 'feat_4', period=15),
    AROON('Aroon', 'feat_3', period=5),
    Decompose('Decompose', 'feat_5'),
    Field('y')
])


data = inline_x_data(data.iloc[:60, :], lookback=5, train=True, dropna=True)


print(data.head(10))