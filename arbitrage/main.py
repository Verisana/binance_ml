import json
from decimal import *
from arbitrage.algo_bot import BinancePriceTunnel
from binance.client import Client
from profiles.models import BinanceKey


bk = BinanceKey.objects.get(name='binance_test')

client = Client(bk.api_key, bk.api_secret)
symbol_info = json.load(open('arbitrage/json/symbol_info.json'))
stepsize_info = json.load(open('arbitrage/json/stepsize_info.json'))
orders = client.get_orderbook_ticker()
bpt = BinancePriceTunnel()

orders_dict = {}
for i in orders:
    orders_dict[i['symbol']] = i

usdt_array = json.load(open('arbitrage/json/tree/usdt_tree.json'))
btc_array = json.load(open('arbitrage/json/tree/btc_tree.json'))
eth_array = json.load(open('arbitrage/json/tree/eth_tree.json'))
bnb_array = json.load(open('arbitrage/json/tree/bnb_tree.json'))

btc_eth_cross = json.load(open('arbitrage/json/cross/btc_eth_cross.json'))
btc_bnb_cross = json.load(open('arbitrage/json/cross/btc_bnb_cross.json'))
btc_usdt_cross = json.load(open('arbitrage/json/cross/btc_usdt_cross.json'))
eth_bnb_cross = json.load(open('arbitrage/json/cross/eth_bnb_cross.json'))
eth_usdt_cross = json.load(open('arbitrage/json/cross/eth_usdt_cross.json'))
bnb_usdt_cross = json.load(open('arbitrage/json/cross/bnb_usdt_cross.json'))
btc_eth_bnb_cross = json.load(open('arbitrage/json/cross/btc_eth_bnb_cross.json'))
btc_eth_usdt_cross = json.load(open('arbitrage/json/cross/btc_eth_usdt_cross.json'))
btc_bnb_usdt_cross = json.load(open('arbitrage/json/cross/btc_bnb_usdt_cross.json'))
eth_bnb_usdt_cross = json.load(open('arbitrage/json/cross/eth_bnb_usdt_cross.json'))
btc_eth_bnb_usdt_cross = json.load(open('arbitrage/json/cross/btc_eth_bnb_usdt_cross.json'))

price_tunnel_result = []

for i in btc_usdt_cross:
    base = i + 'USDT'
    key_1 = i + 'BTC'
    key_2 = 'BTCUSDT'
    price_tunnel_result.append(bpt.check_usdt_tunnel(base, key_1, key_2, orders_dict))

for i in eth_usdt_cross:
    base = i + 'USDT'
    key_1 = i + 'ETH'
    key_2 = 'ETHUSDT'
    price_tunnel_result.append(bpt.check_usdt_tunnel(base, key_1, key_2, orders_dict))

for i in bnb_usdt_cross:
    base = i + 'USDT'
    key_1 = i + 'BNB'
    key_2 = 'BNBUSDT'
    price_tunnel_result.append(bpt.check_usdt_tunnel(base, key_1, key_2, orders_dict))

price_tunnel_result.sort()

for i in price_tunnel_result:
    print(i)
