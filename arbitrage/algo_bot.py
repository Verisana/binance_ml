from decimal import *
from collections import namedtuple


class BinancePriceTunnel:

    def __init__(self):
        pass

    def pay_fee(self, amount):
        fee = Decimal('0.001')
        amount = Decimal(amount)
        return amount - (amount*fee)

    def check_usdt_tunnel(self, base_key, key_1, key_2, orders_dict):
        # noinspection PyTypeChecker
        result_template = namedtuple(base_key, ['roi',
                                                'profit_abs',
                                                'invest_amount',
                                                'return_amount',
                                                'qty',
                                                'base_price',
                                                'symbol_tuple',
                                                ])
        symbol_tuple = (base_key, key_1, key_2)
        getcontext().prec = 8
        #askPrice - red - lowest_buy
        #bidPrice - green - highest_sell
        if Decimal(orders_dict[base_key]['askPrice']) == 0 or Decimal(orders_dict[base_key]['bidPrice']) == 0:
            result = result_template(0,
                                     0,
                                     0,
                                     0,
                                     0,
                                     0,
                                     '{0} not trading anymore'.format(base_key),
                                     )
            return result

        base_price = Decimal(orders_dict[base_key]['askPrice'])
        price_1 = Decimal(orders_dict[key_1]['bidPrice'])
        price_2 = Decimal(orders_dict[key_2]['bidPrice'])

        qty_temp = min(Decimal(orders_dict[base_key]['askQty']),
                       Decimal(orders_dict[key_1]['bidQty']))

        qty_final = min(qty_temp,
                        (Decimal(orders_dict[key_2]['bidQty']) / price_1))

        invest_amount = qty_final * base_price
        temp_return = self.pay_fee(qty_final)
        temp_return = temp_return * price_1
        temp_return = self.pay_fee(temp_return)
        temp_return = temp_return * price_2
        return_amount = self.pay_fee(temp_return)

        profit_abs = return_amount - invest_amount
        roi = ((return_amount - invest_amount) / invest_amount) * 100

        result = result_template(roi,
                                 profit_abs,
                                 invest_amount,
                                 return_amount,
                                 qty_final,
                                 base_price,
                                 symbol_tuple,
                                 )
        return result