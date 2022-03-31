import time
import pybithumb
import datetime

con_key =
sec_key =

bithumb = pybithumb.Bithumb(con_key, sec_key)

#매수주문
def buy_crypto_currency(ticker):
    krw = bithumb.get_balance(ticker)[2]
    sell_price = bithumb.get_current_price(ticker)
    unit = krw/float(sell_price) * 0.7
    return bithumb.buy_market_order(ticker, unit)

#매도주문
def sell_crypto_currency(ticker):
    unit = bithumb.get_balance(ticker)[0]
    return bithumb.sell_market_order(ticker, unit)

#macd구하기
def get_signal(ticker):
    df = pybithumb.get_candlestick(ticker, chart_intervals="1h")

    macd3 = sum(df["close"].tail(12)) / 12
    macd8 = sum(df["close"].tail(26)) / 26
    macd = macd3 - macd8
    macd15 = macd3
    macd40 = macd8

    for i in range(1,9):
        macd15 = macd15 + (sum(df["close"].tail(i+12)) - sum(df["close"].tail(i)))/12
        macd40 = macd40 + (sum(df["close"].tail(i+26)) - sum(df["close"].tail(i)))/26

    macd15 = macd15 / 9
    macd40 = macd40 / 9

    rsi = macd15 - macd40
    macdsig = macd - rsi

    if macdsig > 0 :
        return 1               #매수신호
    elif macdsig <= 0 :
        return 2               #매도신호

# 자동주문
print("시작")
while True:
    try :
        now = datetime.datetime.now()
        if now.minute == 0 and now.second == 0:
            signal = get_signal("BTC")
            if signal == 1 :
                buy_crypto_currency("BTC")
            elif bithumb.get_balance("BTC")[0] != 0 and signal == 2 :
                sell_crypto_currency("BTC")
    except :
        pass
    time.sleep(0.9)