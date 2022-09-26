import selection
import trading
import FinanceDataReader as fdr
import datetime

today_dt = datetime.datetime.today().strftime('%Y-%m-%d')
prev_dt = fdr.DataReader('005930', end = today_dt).index[-2].strftime('%Y-%m-%d')

if __name__ == '__main__':

    select_tops = selection.select_stocks(prev_dt).sort_values(by='yhat', ascending=False).head(5)

    select_dict = {}
    for code in list(select_tops.index):
        s =  select_tops.loc[code]
        select_dict[code] = [s['name'], s['close']]

    print(select_dict)
    trading.auto_trading(select_dict.keys())
