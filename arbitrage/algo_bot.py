from decimal import *
import datetime
from collections import namedtuple
import json
from django.utils import timezone
from binance.client import Client
from info_data.models import AllRealTimeTicker
from arbitrage.models import BotSettings, Deals
import telegram


class BinancePriceTunnel:
    def __init__(self):
        self.bot = BotSettings.objects.all()[0]
        self.symbol_info_key = json.load(open('arbitrage/json/symbol_info_key.json'))
        self.fee_rate = Decimal('0.1') / 100


    def deduct_fee(self, qty):
        qty = Decimal(qty)
        return qty - (qty * self.fee_rate)

    def buy_action(self, ask_price, quantity):
        return quantity / ask_price

    def sell_action(self, bid_price, quantity):
        return quantity * bid_price

    def normalize_lot_size(self, key, qty):
        stepsize = Decimal(self.symbol_info_key[key]['filters'][1]['stepSize'])
        return qty.quantize(stepsize, rounding=ROUND_DOWN)

    def calculate_return(self, qty, price_1, price_2, symbol_tuple, reverse):
        qty = self.deduct_fee(qty)
        qty = self.normalize_lot_size(symbol_tuple[1], qty)
        if not reverse:
            middle_qty = self.sell_action(price_1, qty)
        else:
            middle_qty = self.buy_action(price_1, qty)

        middle_qty = self.normalize_lot_size(symbol_tuple[1], middle_qty)
        middle_qty = self.deduct_fee(middle_qty)
        middle_qty = self.normalize_lot_size(symbol_tuple[2], middle_qty)
        return_amount = self.sell_action(price_2, middle_qty)
        return_amount = self.deduct_fee(return_amount)
        return return_amount

    def check_usdt_tunnel(self, base_key, key_1, key_2, orders_dict, reverse):
        # noinspection PyTypeChecker
        result_template = namedtuple(base_key, ['profit_abs',
                                                'roi',
                                                'invest_amount',
                                                'return_amount',
                                                'qty_final',
                                                'base_price',
                                                'symbol_tuple',
                                                'reverse',
                                                'price_info',
                                                'should_info',
                                                ])
        result = result_template(0, 0, 0, 0, 0, 0, (), reverse, (), ())
        symbol_tuple = (base_key, key_1, key_2)
        #askPrice - red - lowest_buy
        #bidPrice - green - highest_sell

        base_price = orders_dict[base_key].best_ask_pr
        if not reverse:
            price_1 = orders_dict[key_1].best_bid_pr
        else:
            price_1 = orders_dict[key_1].best_ask_pr
        price_2 = orders_dict[key_2].best_bid_pr

        if not base_price or not price_1 or not price_2:
            return result

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

        qty_final = self.normalize_lot_size(base_key, qty_final)

        if not qty_final:
            return result

        invest_amount = qty_final * base_price

        if invest_amount > self.bot.stop_qty and self.bot.stop_qty != 0:
            should_invest = invest_amount
            qty_max_available = qty_final
            should_return = self.calculate_return(qty_max_available, price_1, price_2, symbol_tuple, reverse)
            invest_amount = self.bot.stop_qty
            qty_final = invest_amount / base_price
            qty_final = self.normalize_lot_size(base_key, qty_final)
            should_profit = should_return - should_invest
            should_info = (should_invest, should_return, should_profit)
        else:
            should_info = (0, 0, 0)

        return_amount = self.calculate_return(qty_final, price_1, price_2, symbol_tuple, reverse)

        profit_abs = return_amount - invest_amount
        if invest_amount != 0:
            roi = ((return_amount - invest_amount) / invest_amount) * 100
        else:
            roi = 0
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
                                 should_info,
                                 )
        return result


class ExecutePriceTunnel:
    TREE_SYMBOLS = ['BTC', 'ETH', 'BNB', 'USDT']

    def __init__(self):
        self.symbol_info_list = json.load(open('arbitrage/json/symbol_info_list.json'))
        self.symbol_info_key = json.load(open('arbitrage/json/symbol_info_key.json'))
        self.bpt = BinancePriceTunnel()
        self.symbols_usdt = AllRealTimeTicker.objects.filter(symbol_tree='USDT')
        self.symbols_except_usdt = AllRealTimeTicker.objects.exclude(symbol_tree='USDT')
        self.usdt_list = []
        for i in self.symbols_usdt:
            self.usdt_list.append(i.symbol)

    def check_key_2_validity(self, symbol, base):
        if symbol in self.usdt_list and base not in symbol:
            return True
        else:
            return False

    def check_usdt_simple(self):
        orders_dict = {}
        symbols = AllRealTimeTicker.objects.all()
        for i in symbols:
            orders_dict[i.symbol] = i
        price_tunnel_result = []

        for symbol_usdt in self.symbols_usdt:
            for symbol_cross in self.symbols_except_usdt:
                base = symbol_usdt.symbol
                base_baseasset = self.symbol_info_key[base]['baseAsset']
                if base_baseasset in self.TREE_SYMBOLS and base_baseasset in symbol_cross.symbol:
                    key_1 = symbol_cross.symbol
                    if base_baseasset == self.symbol_info_key[key_1]['baseAsset']:
                        key_2 = self.symbol_info_key[key_1]['quoteAsset'] + 'USDT'
                        if self.check_key_2_validity(key_2, base_baseasset):
                            price_tunnel_result.append(self.bpt.check_usdt_tunnel(base, key_1, key_2, orders_dict, reverse=False))
                    else:
                        key_2 = self.symbol_info_key[key_1]['baseAsset'] + 'USDT'
                        if self.check_key_2_validity(key_2, base_baseasset):
                            price_tunnel_result.append(self.bpt.check_usdt_tunnel(base, key_1, key_2, orders_dict, reverse=True))
                elif base_baseasset in symbol_cross.symbol:
                    key_1 = symbol_cross.symbol
                    key_2 = self.symbol_info_key[key_1]['baseAsset'] + 'USDT'
                    if self.check_key_2_validity(key_2, base_baseasset):
                        price_tunnel_result.append(self.bpt.check_usdt_tunnel(base, key_1, key_2, orders_dict, reverse=False))


        price_tunnel_result.sort()
        return price_tunnel_result


class PriceTunnelTrader:

    def __init__(self, tunnels):
        self.bot = BotSettings.objects.all()[0]
        self.telegram_bot = telegram.Bot(token=self.bot.telegram_bot.token)
        self.tech_chat = self.bot.telegram_bot.chat.get(name='Binance_Tech_Vice_Trader_chat')
        self.info_chat = self.bot.telegram_bot.chat.get(name='Binance_Vice_Trader_chat')
        self.tunnels = tunnels
        self.client = Client(self.bot.binance_api.api_key, self.bot.binance_api.api_secret)
        self.profit_threshold = self.bot.profit_threshold


    def init_trade(self, tunnel):
        new_trade = Deals.objects.create(base_pair=tunnel.symbol_tuple[0],
                                         middle_pair=tunnel.symbol_tuple[1],
                                         end_pair=tunnel.symbol_tuple[2],

                                         init_qty=tunnel.qty_final,

                                         expected_base_price=tunnel.price_info[0],
                                         expected_middle_price=tunnel.price_info[1],
                                         expected_end_price=tunnel.price_info[2],

                                         reverse=tunnel.reverse,
                                         expected_invest_amount=tunnel.invest_amount,
                                         expected_profit=tunnel.profit_abs,
                                         expected_return=tunnel.return_amount,
                                         expected_roi=tunnel.roi)
        self.place_base_order(new_trade)

    def place_base_order(self, trade):
        order = self.client.create_order(symbol=trade.base_pair,
                                         side='BUY',
                                         type='LIMIT',
                                         timeInForce='IOC',
                                         quantity=1,
                                         price=1)
        if order['status'] == 'FILLED':
            trade.base_order_id = order['clientOrderId']
            trade.invest = order['cummulativeQuoteQty']
            trade.datetime_base_pair = datetime.datetime.utcfromtimestamp(int(order['transactTime'])/1000).replace(tzinfo=timezone.get_current_timezone())

            trade.save()

    def place_middle_order(self):
        pass

    def place_end_order(self):
        pass

    def _is_repeated_deal(self, symbol_tuple, price_tuple, init_qty):
        now = timezone.now()
        deals = Deals.objects.filter(date_open__range=(now - timezone.timedelta(minutes=1), now))
        init_hash = hash(
                         (
                            symbol_tuple[0],
                            symbol_tuple[1],
                            symbol_tuple[2],

                            price_tuple[0],
                            price_tuple[1],
                            price_tuple[2],

                            init_qty,
                         )
                        )
        if deals:
            for deal in deals:
                check_hash = hash(
                    (
                        deal.base_pair,
                        deal.middle_pair,
                        deal.end_pair,

                        deal.base_price,
                        deal.middle_price,
                        deal.end_price,

                        deal.init_qty,
                    )

                )
                if check_hash == init_hash:
                    return True
        return False

    def check_profit_trade(self):
        for tunnel in self.tunnels[::-1]:
            repeated_trade = self._is_repeated_deal(tunnel.symbol_tuple, tunnel.price_info, tunnel.qty_final)
            if tunnel.profit_abs > self.profit_threshold and tunnel.invest_amount > 10 and not repeated_trade:
                self.inform_telegram(tunnel)
                #self.init_trade(tunnel)
            #Result already sorted, if no profit, break
            elif tunnel.invest_amount < 10:
                continue
            else:
                break


    def inform_telegram(self, tunnel):
        deal = Deals.objects.create(
                                            base_pair=tunnel.symbol_tuple[0],
                                            middle_pair=tunnel.symbol_tuple[1],
                                            end_pair=tunnel.symbol_tuple[2],

                                            init_qty=tunnel.qty_final,

                                            expected_base_price=tunnel.price_info[0],
                                            expected_middle_price=tunnel.price_info[1],
                                            expected_end_price=tunnel.price_info[2],

                                            reverse=tunnel.reverse,

                                            expected_invest=tunnel.invest_amount,
                                            expected_return=tunnel.return_amount,
                                            expected_roi=tunnel.roi,
                                            expected_profit=tunnel.profit_abs,

                                            hypothetical_invest=tunnel.should_info[0],
                                            hypothetical_return=tunnel.should_info[1],
                                            hypothetical_profit=tunnel.should_info[2],
        )

        message = '''Есть сделка в плюс
ROI = {0} %
Ожидаемый профит = {1} $ 
Схема = {2}
Инвест = {3} $
Возврат = {4} $
'''.format(round(tunnel.roi, 2),
                   round(tunnel.profit_abs, 8),
                   tunnel.symbol_tuple,
                   round(tunnel.invest_amount, 8),
                   round(tunnel.return_amount, 8))
        while True:
            try:
                #print(tunnel)
                self.telegram_bot.send_message(self.tech_chat.chat_id, message)
            except:
                continue
            break