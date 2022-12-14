
# install ta library before execution of the codes with 'pip install ta'
# import ta
from math import log
from pandas import DataFrame

class Candle(int):
	"""
	Candle object is simply an index of a list/array which is composed of
	dict components returned by IQoption API
	"""
    def __new__(cls, index, data):
        if index < len(data) and data[index]:
            return super().__new__(cls, index)

    def __init__(self, index, data):
        int.__init__(index)
        self.data = data
        self.min = data[index]['min'] # change min,max with high,low if nessesary
        self.max = data[index]['max']
        self.open = data[index]['open']
        self.vol = self.data[index]['volume']
        self.close = data[index]['close']


"""
Remember indicators return nan or None for the candles that come
before the period. e.g. if the period is 14, then the 13 first values 
of the indicator function output will be None or nan.
"""




def LSMA(data, window: int) -> DataFrame:
	"""
	LSMA is the Least Square Moving Average
	The 'data' can be any list of numbers e.g. high, close , etc.
	'window' is the period of indication
  data can be a pandas series or list of floats or ints
	"""

    ma_data = data
    pl = []
    lr = []
    
    for i in range(len(ma_data)):
        
        pl.append(float(ma_data[i]));

        if(len(pl) >= window):
            sum_x = 0.0; sum_y = 0.0; sum_xy = 0.0; sum_xx = 0.0; sum_yy = 0.0;

            for a in range(1, len(pl)+1):
                sum_x += a;
                sum_y += pl[a-1];
                sum_xy += (pl[a-1] * a);
                sum_xx += (a*a);
                sum_yy += (pl[a-1] * pl[a-1]);

            m = ((sum_xy - sum_x * sum_y / window) / (sum_xx - sum_x * sum_x / window));
            b = sum_y / window - m * sum_x / window;
            lr.append(m * window + b);
            pl = pl[1:];

        else:
          lr.append(None);

    return DataFrame(lr)


def GOPA(candles: list, period: int) -> DataFrame:
  """
  Gopalakrishnan range index indicator
  Moves exactly in the opposite direction of trend 
  candles is a json-like list of candles with the keys "open","max","min","close"
  max and min value of each candle is accessed using syntax like dictionary['key']
  """

  l = []
  for i in range(len(candles)):
    if i >= period:
      _min = min([c['min'] for c in data[i-period:i]])
      _max = max([c['max'] for c in data[i-period:i]])
      if (_max - _min) != 0:
        gopa = round(log(abs(_max - _min))/period,6)
      elif _max - _min == 0:
        gopa = 0

      # print(i)
    else:
      gopa = None
    l.append(gopa)
  return DataFrame(l)


def heiken_ashi(data:list ,candle=True) -> DataFrame:
	"""
	creates a list of heiken-ashi's 
	"""
	_l = []

	ashi = {'close' : (data[0]['close'] + data[0]['open'] + data[0]['min']+data[0]['max'])/4 ,
	    'open' : (data[0]['close']+data[0]['open'])/2,
	    'max' : max(data[0]['max'],(data[0]['close']+data[0]['open']+data[0]['min']+data[0]['max'])/4 ,(data[0]['close']+data[0]['open'])/2),
	    'min' : min(data[0]['max'],(data[0]['close']+data[0]['open']+data[0]['min']+data[0]['max'])/4 ,(data[0]['close']+data[0]['open'])/2)
	    }
	_l.append(ashi)

	for i in range(1,len(data)):
	ashi = {'close' : (data[i]['close'] + data[i]['open'] + data[i]['min']+data[i]['max'])/4 ,
	        'open' : (_l[i-1]['close']+_l[i-1]['open'])/2,
	        'max' : max(data[i]['max'],(data[i]['close']+data[i]['open']+data[i]['min']+data[i]['max'])/4 ,(_l[i-1]['close']+_l[i-1]['open'])/2,),
	        'min' : min(data[i]['max'],(data[i]['close']+data[i]['open']+data[i]['min']+data[i]['max'])/4 ,(_l[i-1]['close']+_l[i-1]['open'])/2,)
	        }
	_l.append(ashi)

	return DataFrame(_l)



############### Some indocators from ta ##############################
"""
ta library docs:
https://technical-analysis-library-in-python.readthedocs.io/en/latest/ta.html


RSI = ta.momentum.RSIIndicator(close: pandas.core.series.Series, window: int = 14, fillna: bool = False).rsi()
EMA = ta.trend.EMAIndicator(close: pandas.core.series.Series, window: int = 14, fillna: bool = False)

"""
