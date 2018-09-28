import json
from binance.client import Client


client = Client('0', '0')
exchange_info = client.get_exchange_info()
symbol_info_list = []
rate_limits = exchange_info['rateLimits']
symbol_info_key = dict()
bnb_tree, btc_tree, eth_tree, usdt_tree = [], [], [], []

for info in exchange_info['symbols']:
    if info['status'] == 'TRADING':
        if 'BNB' in info['symbol'][-4:]:
            bnb_tree.append(info['symbol'])
        elif 'BTC' in info['symbol'][-4:]:
            btc_tree.append(info['symbol'])
        elif 'ETH' in info['symbol'][-4:]:
            eth_tree.append(info['symbol'])
        else:
            usdt_tree.append(info['symbol'])
        symbol_info_list.append(info)
        symbol_info_key[info['symbol']] = info

with open('arbitrage/json/symbol_info_list.json', 'w') as outfile:
    json.dump(symbol_info_list, outfile)
with open('arbitrage/json/symbol_info_key.json', 'w') as outfile:
    json.dump(symbol_info_key, outfile)
with open('arbitrage/json/rate_limits.json', 'w') as outfile:
    json.dump(rate_limits, outfile)


with open('arbitrage/json/tree/bnb_tree.json', 'w') as outfile:
    json.dump(bnb_tree, outfile)
with open('arbitrage/json/tree/btc_tree.json', 'w') as outfile:
    json.dump(btc_tree, outfile)
with open('arbitrage/json/tree/eth_tree.json', 'w') as outfile:
    json.dump(eth_tree, outfile)
with open('arbitrage/json/tree/usdt_tree.json', 'w') as outfile:
    json.dump(usdt_tree, outfile)