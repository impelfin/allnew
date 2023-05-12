import pandas_datareader as pdr
from datetime import datetime

print(pdr.__version__)

start = datetime(2016, 2, 19)
end = datetime(2016, 3, 4)

df = pdr.DataReader("078930.KS", "yahoo", start, end)

print(type(df))