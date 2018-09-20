from decimal import *
from collections import namedtuple
import json
from binance.client import Client
from info_data.models import AllRealTimeTicker
from arbitrage.models import BotSettings, OpenedDeals
import telegram


class BinancePriceTunnel:
    def __init__(self):
        self.bot = BotSettings.objects.all()[0]

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
                                                'price_info',
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

        if not self.bot.stop_qty >= invest_amount:
            #should_invest = invest_amount
            #qty_max_available = qty_final
            invest_amount = self.bot.stop_qty
            qty_final = invest_amount / base_price

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
        price_info = (base_price, price_1, price_2)

        result = result_template(profit_abs,
                                 roi,
                                 invest_amount,
                                 return_amount,
                                 qty_final,
                                 base_price,
                                 symbol_tuple,
                                 reverse,
                                 price_info,
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


class PriceTunnelTrader:
    PROFIT_THRESHOLD = 0.1

    def __init__(self, tunnels):
        self.bot = BotSettings.objects.all()[0]
        self.telegram_bot = telegram.Bot(token=self.bot.telegram_bot.token)
        self.tech_chat = self.bot.telegram_bot.chat.get(name='Binance_Tech_Vice_Trader_chat')
        self.info_chat = self.bot.telegram_bot.chat.get(name='Binance_Vice_Trader_chat')
        self.tunnels = tunnels
        self.client = Client(self.bot.binance_api.api_key, self.bot.binance_api.api_secret)


    def init_trade(self, tunnel):


        new_trade = OpenedDeals.objects.create(base_pair=tunnel.symbol_tuple[0],
                                               middle_pair=tunnel.symbol_tuple[1],
                                               end_pair=tunnel.symbol_tuple[2],

                                               qty_to_trade=tunnel.qty_final,

                                               base_price=tunnel.price_info[0],
                                               middle_price=tunnel.price_info[1],
                                               end_price=tunnel.price_info[2],

                                               is_reverse=tunnel.reverse,
                                               invest_amount=tunnel.invest_amount,
                                               expected_profit=tunnel.profit_abs,
                                               expected_return=tunnel.return_amount,
                                               expected_roi=tunnel.roi)
        self.place_base_order(new_trade)

    def place_base_order(self, trade):
        if not trade.is_base_order_set:
            self.client.create_order(symbol=trade.base_pair,
                                     side='BUY',
                                     type='LIMIT',
                                     timeInForce='IOC',
                                     quantity=1,
                                     price=1)

    def place_middle_order(self):
        pass

    def place_end_order(self):
        pass

    def check_profit_trade(self):
        for tunnel in self.tunnels[::-1]:
            if tunnel.profit_abs >= self.PROFIT_THRESHOLD:
                self.inform_telegram(tunnel)
                self.init_trade(tunnel)
            #Result already sorted, if no profit, break
            else:
                break


    def inform_telegram(self, tunnel):
        message = '''Есть сделка в плюс
ROI = {0} %
Ожидаемый профит = {1} $ 
Схема = {2}
Инвест = {3} $
Возврат = {4} $
'''.format(round(tunnel.roi, 2),
                   round(tunnel.profit_abs, 2),
                   tunnel.symbol_tuple,
                   round(tunnel.invest_amount, 2),
                   round(tunnel.return_amount, 2))
        while True:
            try:
                self.telegram_bot.send_message(self.tech_chat.chat_id, message)
            except:
                continue
            print(message)
            break