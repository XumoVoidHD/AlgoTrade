import talib
import pandas as pd
import yfinance as yf
from backtesting import Backtest, Strategy
from backtesting.lib import crossover
from backtesting.test import SMA, GOOG

class rsi_ema_strategy(Strategy):

    def init(self):
        price = self.data.Close
        self.rsi = self.I(talib.RSI, price)
        self.ma1 = self.I(SMA, price, 20)
        self.ma2 = self.I(SMA, price, 50)
        self.atr = self.I(talib.ATR, data.High, data.Low, data.Close, timeperiod=14)
        with pd.option_context('display.max_rows', None, 'display.max_columns', None):
            print(data)

    def next(self):
        price = self.data.Close[-1]
        atr_value = self.atr[-1]

        take_profit = price + 3 * atr_value
        stop_loss = price - 1.5 * atr_value
        if crossover(30, self.rsi) or crossover(self.ma1, self.ma2):
            self.buy(tp= take_profit, sl= stop_loss)
        elif crossover(self.rsi, 70) or crossover(self.ma2, self.ma1):
            self.position.close()


data = yf.download("AAPL", "2020-04-04","2024-04-04" )
backtest = Backtest(data, rsi_ema_strategy, commission=0.002, exclusive_orders=True)
stats = backtest.run()
print(stats)
backtest.plot()

class MyMACDStrategy(Strategy):

    def init(self):
        price = self.data.Close
        self.macd = self.I(lambda x: talib.MACD(x)[0], price)
        self.macd_signal = self.I(lambda x: talib.MACD(x)[1], price)
        print(self.macd_signal)

    def next(self):
        if crossover(self.macd, self.macd_signal):
            self.buy()
        elif crossover(self.macd_signal, self.macd):
            self.sell()


# data = yf.download("AAPL", "2020-04-04","2024-04-04" )
# backtest = Backtest(data, MyMACDStrategy, commission=0.002, exclusive_orders=True)
# stats = backtest.run()
# print(stats)


class MySMAStrategy(Strategy):

    def init(self):
        price = self.data.Close
        self.ma1 = self.I(SMA, price, 10)
        self.ma2 = self.I(SMA, price, 20)

    def next(self):
        if crossover(self.ma1, self.ma2):
            self.buy()
        elif crossover(self.ma2, self.ma1):
            self.sell()

#
# backtest = Backtest(GOOG, MySMAStrategy, commission=0.002, exclusive_orders=True)
# stats = backtest.run()
# print(stats)
