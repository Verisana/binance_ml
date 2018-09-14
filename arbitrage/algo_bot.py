from decimal import *
from collections import namedtuple
import json
from info_data.models import AllRealTimeTicker


class BinancePriceTunnel:
    def __init__(self):
        pass

    def pay_fee(self, amount):
        fee = Decimal('0.001')
        amount = Decimal(amount)
        return amount - (amount*fee)

    def buy_action(self, bid_price, quantity):
        return quantity / bid_price

    def sell_action(self, ask_price, quantity):
        return quantity * ask_price

    def check_usdt_tunnel(self, base_key, key_1, key_2, orders_dict, reverse):
        # noinspection PyTypeChecker
        result_template = namedtuple(base_key, ['profit_abs',
                                                'roi',
                                                'invest_amount',
                                                'return_amount',
                                                'qty',
                                                'base_price',
                                                'symbol_tuple',
                                                'reverse',
                                                ])
        symbol_tuple = (base_key, key_1, key_2)
        #askPrice - red - lowest_buy
        #bidPrice - green - highest_sell

        base_price = orders_dict[base_key].best_ask_pr
        if not reverse:
            price_1 = orders_dict[key_1].best_bid_pr
        else:
            price_1 = orders_dict[key_1].best_ask_pr
        price_2 = orders_dict[key_2].best_bid_pr

        if not reverse:
            qty_temp = min(orders_dict[base_key].best_ask_qty,
                           orders_dict[key_1].best_bid_qty)

            qty_final = min(qty_temp,
                            (orders_dict[key_2].best_bid_qty / price_1))
        else:
            qty_temp = min(orders_dict[base_key].best_ask_qty / price_1,
                           orders_dict[key_1].best_ask_qty)

            qty_final = min(qty_temp,
                            orders_dict[key_2].best_bid_qty) * price_1

        invest_amount = qty_final * base_price

        temp_return = self.pay_fee(qty_final)

        if not reverse:
            temp_return = self.sell_action(price_1, temp_return)
        else:
            temp_return = self.buy_action(price_1, temp_return)

        temp_return = self.pay_fee(temp_return)
        temp_return = self.sell_action(price_2, temp_return)
        return_amount = self.pay_fee(temp_return)

        profit_abs = return_amount - invest_amount
        roi = ((return_amount - invest_amount) / invest_amount) * 100

        result = result_template(profit_abs,
                                 roi,
                                 invest_amount,
                                 return_amount,
                                 qty_final,
                                 base_price,
                                 symbol_tuple,
                                 reverse,
                                 )
        return result


class ExecutePriceTunnel:
    TREE_SYMBOLS = ['BTC', 'ETH', 'BNB', 'USDT']

    def __init__(self):
        #self.bk = BinanceKey.objects.get(name='binance_test')
        #self.client = Client(self.bk.api_key, self.bk.api_secret)
        self.symbol_info = json.load(open('arbitrage/json/symbol_info.json'))
        self.stepsize_info = json.load(open('arbitrage/json/stepsize_info.json'))
        self.bpt = BinancePriceTunnel()


    def check_usdt_simple(self):
        orders_dict = {}
        symbols = AllRealTimeTicker.objects.all()
        symbols_except_usdt = AllRealTimeTicker.objects.exclude(symbol_tree='USDT')
        for i in symbols:
            orders_dict[i.symbol] = i
        price_tunnel_result = []
        symbols_usdt = AllRealTimeTicker.objects.filter(symbol_tree='USDT')
        usdt_list = []
        for i in symbols_usdt:
            usdt_list.append(i.symbol)

        for symbol_usdt in symbols_usdt:
            for symbol_cross in symbols_except_usdt:
                base = symbol_usdt.symbol

                if base[0:-4] in self.TREE_SYMBOLS and base[0:-4] in symbol_cross.symbol:
                    key_1 = symbol_cross.symbol
                    key_2 = symbol_cross.symbol.replace(base[0:-4], '') + 'USDT'
                    if key_2 in usdt_list:
                        if key_2[0:-4] not in self.TREE_SYMBOLS:
                            price_tunnel_result.append(self.bpt.check_usdt_tunnel(base, key_1, key_2, orders_dict, reverse=True))
                        else:
                            price_tunnel_result.append(self.bpt.check_usdt_tunnel(base, key_1, key_2, orders_dict, reverse=False))
                elif base[0:-4] in symbol_cross.symbol:
                    key_1 = symbol_cross.symbol
                    key_2 = symbol_cross.symbol.replace(base[0:-4], '') + 'USDT'
                    if key_2 in usdt_list:
                        price_tunnel_result.append(self.bpt.check_usdt_tunnel(base, key_1, key_2, orders_dict, reverse=False))


        price_tunnel_result.sort()
        return price_tunnel_result

'''
usdt_array = json.load(open('arbitrage/json/tree/usdt_tree.json'))
btc_array = json.load(open('arbitrage/json/tree/btc_tree.json'))
eth_array = json.load(open('arbitrage/json/tree/eth_tree.json'))
bnb_array = json.load(open('arbitrage/json/tree/bnb_tree.json'))

btc_eth_cross = json.load(open('arbitrage/json/cross/btc_eth_cross.json'))
btc_bnb_cross = json.load(open('arbitrage/json/cross/btc_bnb_cross.json'))
eth_bnb_cross = json.load(open('arbitrage/json/cross/eth_bnb_cross.json'))
btc_eth_bnb_cross = json.load(open('arbitrage/json/cross/btc_eth_bnb_cross.json'))
btc_eth_usdt_cross = json.load(open('arbitrage/json/cross/btc_eth_usdt_cross.json'))
btc_bnb_usdt_cross = json.load(open('arbitrage/json/cross/btc_bnb_usdt_cross.json'))
eth_bnb_usdt_cross = json.load(open('arbitrage/json/cross/eth_bnb_usdt_cross.json'))
btc_eth_bnb_usdt_cross = json.load(open('arbitrage/json/cross/btc_eth_bnb_usdt_cross.json'))

btc_usdt_cross = json.load(open('arbitrage/json/cross/btc_usdt_cross.json'))
eth_usdt_cross = json.load(open('arbitrage/json/cross/eth_usdt_cross.json'))
bnb_usdt_cross = json.load(open('arbitrage/json/cross/bnb_usdt_cross.json'))
'''