#importing yfinance module to fetch and download histrocial data from yahoo finance
import yfinance as yf
#importing pandas module to use data manipulation and analysis
import pandas as pd
#importing ta maodule to do technical analysis
import ta
#importing matplotlib to data visulization 
import matplotlib.pyplot as plt


#donwloading histrocial data

start_date ='2023-01-01'
end_date='2024-09-30'
#downloading the data from yahoo finace
data=yf.download('EURINR=X',start=start_date ,end=end_date)

# Calculate technical indicators
data['MA_50']=data['Close'].rolling(window=50).mean()#50-day moving average of the closing price.
data['MA_200']=data['Close'].rolling(window=200).mean()#200-day moving average of the closing price.

#20-day Bollinger Bands (upper and lower bands).

data['BB_upper']=data['Close'].rolling(window=20).mean()+2*data['Close'].rolling(window=20).std()
data['BB_lower']=data['Close'].rolling(window=20).mean()-2*data['Close'].rolling(window=20).std()

#14 day Commodity Channel Index

data['CCI']=ta.trend.cci(data['High'],data['Low'],data['Close'],window=14)

# Calculate technical indicators for one day and one week from sept 30,2024
#calculates the technical indicators for the last day and the last week of the data.
one_day_data=data.iloc[-1:]
one_week_data=data.iloc[-5:-1]

one_day_ma_50 = one_day_data['MA_50'].values[0]
one_day_ma_200 = one_day_data['MA_200'].values[0]
one_day_bb_upper = one_day_data['BB_upper'].values[0]
one_day_bb_lower = one_day_data['BB_lower'].values[0]
one_day_cci = one_day_data['CCI'].values[0]

one_week_ma_50 = one_week_data['MA_50'].mean()
one_week_ma_200 = one_week_data['MA_200'].mean()
one_week_bb_upper = one_week_data['BB_upper'].mean()
one_week_bb_lower = one_week_data['BB_lower'].mean()
one_week_cci = one_week_data['CCI'].mean()

# Make a decision based on technical indicators
def make_decision(ma_50, ma_200, bb_upper, bb_lower, cci):
    if ma_50 > ma_200 and cci > 100:
        return 'BUY'
    elif ma_50 < ma_200 and cci < -100:
        return 'SELL'
    else:
        return 'NEUTRAL'

one_day_decision = make_decision(one_day_ma_50, one_day_ma_200, one_day_bb_upper, one_day_bb_lower, one_day_cci)
one_week_decision = make_decision(one_week_ma_50, one_week_ma_200, one_week_bb_upper, one_week_bb_lower, one_week_cci)

print('One day from Sept 30, 2024:')
print(f'MA_50: {one_day_ma_50:.2f}')
print(f'MA_200: {one_day_ma_200:.2f}')
print(f'BB_upper: {one_day_bb_upper:.2f}')
print(f'BB_lower: {one_day_bb_lower:.2f}')
print(f'CCI: {one_day_cci:.2f}')
print(f'Decision: {one_day_decision}')

print('\nOne week from Sept 30, 2024:')
print(f'MA_50: {one_week_ma_50:.2f}')
print(f'MA_200: {one_week_ma_200:.2f}')
print(f'BB_upper: {one_week_bb_upper:.2f}')
print(f'BB_lower: {one_week_bb_lower:.2f}')
print(f'CCI: {one_week_cci:.2f}')
print(f'Decision: {one_week_decision}')

# Visualize the data
plt.figure(figsize=(12,6))
plt.plot(data['Close'], label='Close Price')
plt.plot(data['MA_50'], label='MA 50')
plt.plot(data['MA_200'], label='MA 200')
plt.plot(data['BB_upper'], label='BB Upper')
plt.plot(data['BB_lower'], label='BB Lower')
plt.legend(loc='best')
plt.title('EUR/INR Currency Pair Technical Analysis')
plt.xlabel('Date')
plt.ylabel('Price')
plt.show()
