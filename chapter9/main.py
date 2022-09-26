import selection
import trading

today_dt = '2022-09-23'

if __name__ == '__main__':
    
    select_tops = selection.select_stocks(today_dt).sort_values(by='yhat', ascending=False).head(5)

    select_dict = {}
    for code in list(select_tops.index):
        s =  select_tops.loc[code]
        select_dict[code] = [s['name'], s['close']]       

    print(select_dict)

    trading.auto_trading(select_dict.keys())