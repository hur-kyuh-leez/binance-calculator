# Written By Hercules
# This does NOT take deposits and withdrawals into account, only trade history
# Make sure your api keys can only be used by your IP and disable withdraw
# This code ignores BNB coin
## Remember to change three variables: public_api, secret_api, trade_after_this_date


import binance as b # python binance api, credit to https://github.com/toshima/binance   Thank you toshima!!
from datetime import date



## write down your api
#examples:
#public_api = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
#secret_api = "bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb"

public_api = ""
secret_api = ""
b.set(public_api, secret_api)

def binance_clock_cal(year, month, days):
    binance_birthday = date(1970, 01,01)
    today = date(year, month, days)
    days_difference = (today - binance_birthday).days
    binance_time = days_difference * 24*60*60000 #there are extra 000 after 'seconds(s)' place
    return binance_time



## change date of your choice
trade_after_this_date = binance_clock_cal(1991,03,19)


summary = []
profit_list = []
def profit_calculator(market_type):


    try:
        for error in b.myTrades(market_type):
            if error == "msg":
                if "ETH" not in market_type:
                    market_type.replace("BTC","ETH")
                else:
                    market_type.replace("ETH","BTC")
        trade_data = b.myTrades(market_type)
        #trade_data return example
        #[{u'orderId': 46584195, u'isBuyer': True, u'price': u'0.00000927', u'isMaker': True, u'qty': u'900.00000000', u'commission': u'0.90000000', u'time': 1525044165320, u'commissionAsset': u'TRX', u'id': 25242895, u'isBestMatch': True}]
        index = 0
        total_bought_revenue = float(0)
        total_bought_qty = float(0)
        bought_price = float(0)
        while len(trade_data) > index:
            if trade_data[index]["isBuyer"] == True and int(trade_data[index]['time']) >= trade_after_this_date:
                bought_price = float(trade_data[index]["price"])

            if trade_data[index]["isMaker"] == True and int(trade_data[index]['time']) >= trade_after_this_date:
                bought_price = -float(trade_data[index]["price"])

            bought_qty = float(trade_data[index]["qty"])
            total_bought_qty += bought_qty
            bought_revenue = bought_price * bought_qty

            total_bought_revenue += bought_revenue
            index+=1



        avg_bought_price = (total_bought_revenue/total_bought_qty) * float(1.02) #0.02 is for comission


        if avg_bought_price >= float(0.000001):
            avg_bought_price = float(0)

        #getting price for specific coin
        current_price = float(b.prices()[market_type])


        #calculating profit is percentage
        profit = ((current_price / avg_bought_price) - 1) * 100


        # print "%s profit is "%market_type + str(profit) +str(" %")
        if market_type not in summary:
            summary.append(market_type)
        if profit not in profit_list: #problem : this makes error if prices changes very quickly!
            profit_list.append(profit)

        return market_type, profit

    except ZeroDivisionError as Zero_Division_Error:
        return str("Try_different_market")







balance_data = b.balances()
for coin_type in balance_data:
    if float(balance_data["%s"%coin_type]['free']) >= float(0.000001) or float(balance_data["%s"%coin_type]['locked']) >= float(0.000001) : # if there are some amount to the coin_type
        coin_type_BTC = str("%sBTC")%coin_type
        if coin_type_BTC == "BTCBTC":
            continue
        coin_type_BTC_data = profit_calculator(coin_type_BTC)

        if coin_type_BTC_data == "Try_different_market":

            coin_type_ETH = str("%sETH")%coin_type
            if coin_type_ETH == "ETHETH":
                continue

            profit_calculator(coin_type_ETH)




counter = int(0)
while len(summary) > counter:
    if summary[counter] != 'BNBETH' and summary[counter] != 'BNBBTC':
        print(str(summary[counter]) +" "+ str("%.2f"%profit_list[counter]) + "%")
    counter += 1

















