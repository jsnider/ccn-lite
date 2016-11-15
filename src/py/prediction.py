# ccn-lite/src/py/prediction.py

'''
Copyright (C) 2015, Wang Eric Bear, Uppsala University

Permission to use, copy, modify, and/or distribute this software for any
purpose with or without fee is hereby granted, provided that the above
copyright notice and this permission notice appear in all copies.

THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

File history:
2015-11-15 created

Setup:

0) install pip
	sudo python -m pip install --upgrade pip
1) install pandas and a bunch of stuff, take 3-4 minutes to run
	pip install --user numpy scipy matplotlib ipython jupyter pandas sympy nose
2) add export PATH="$PATH:/home/your_user/.local/bin" to path
	
3) instal this one too
	sudo apt-get install python-tk
4) and this one
	python -mpip install statsmodels
5) 
'''
import pandas as pd
import numpy as np
import matplotlib.pylab as plt
from matplotlib.pylab import rcParams
rcParams['figure.figsize'] = 15, 6
from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.stattools import acf,pacf
from statsmodels.tsa.arima_model import ARIMA

#setup date format
dateparse = lambda dates: pd.datetime.strptime(dates, '%Y%m%d') 

data=pd.read_csv('data.csv')
print data.head()


time_series=data['#Play']
print "time series data"
print time_series.head(10)
#plt.plot(time_series)
#plt.show()


#put time series through numpy, 
time_series_log=np.log(time_series)
#plt.plot(time_series_log)
#plt.show()
print "time series log"
print time_series_log


moving_avg=pd.rolling_mean(time_series_log,365)
ts_log_moving_avg_diff=time_series_log-moving_avg
ts_log_moving_avg_diff.dropna(inplace=True)
ts_log_diff=time_series_log-time_series_log.shift()
ts_log_diff.dropna(inplace=True)


lag_acf=acf(ts_log_diff,nlags=100)
lag_pacf=pacf(ts_log_diff,nlags=100,method='ols')


plt.subplot(121)
plt.plot(lag_acf)
plt.axhline(y=0,linestyle='--',color='gray')
plt.axhline(y=-1.96/np.sqrt(len(ts_log_diff)),linestyle='--',color='gray')#lowwer CI
plt.axhline(y=1.96/np.sqrt(len(ts_log_diff)),linestyle='--',color='gray')#upper CI
plt.title('Autocorrelation Function')

plt.subplot(122)
plt.plot(lag_pacf)
plt.axhline(y=0,linestyle='--',color='gray')
plt.axhline(y=-1.96/np.sqrt(len(ts_log_diff)),linestyle='--',color='gray')
plt.axhline(y=1.96/np.sqrt(len(ts_log_diff)),linestyle='--',color='gray')
plt.title('Partial Autocorrelation Function')
plt.tight_layout()
#plt.show()

print "x time series log start"
print time_series_log
print "time series log end"

#order p d q
model=ARIMA(time_series_log,order=(0,1,0))

'''
result_ARIMA=model.fit(disp=-1)
predictions_ARIMA_diff=pd.Series(result_ARIMA.fittedvalues,copy=True)
predictions_ARIMA_diff_cumsum=predictions_ARIMA_diff.cumsum()
predictions_ARIMA_log=pd.Series(time_series_log.ix[0],index=time_series_log.index)
predictions_ARIMA_log=predictions_ARIMA_log.add(predictions_ARIMA_diff_cumsum,fill_value=0)
predictions_ARIMA=np.exp(predictions_ARIMA_log)
plt.plot(ts)
plt.plot(predictions_ARIMA,color='red')
plt.title('RMSE: %.4f'% np.sqrt(sum((predictions_ARIMA-ts)**2)/len(ts)))
plt.show()

'''