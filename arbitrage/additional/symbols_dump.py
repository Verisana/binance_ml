import json
from binance.client import Client


client = Client('0', '0')
exchange_info = client.get_exchange_info()

symbol_info = exchange_info['symbols']
rate_limits = exchange_info['rateLimits']
stepsize_info = dict()
bnb_tree, btc_tree, eth_tree, usdt_tree = [], [], [], []

for info in exchange_info['symbols']:
    stepsize_info[info['symbol']] = info['filters'][1]['minQty']
    if 'BNB' in info['symbol'][-4:]:
        bnb_tree.append(info['symbol'])
    elif 'BTC' in info['symbol'][-4:]:
        btc_tree.append(info['symbol'])
    elif 'ETH' in info['symbol'][-4:]:
        eth_tree.append(info['symbol'])
    elif 'USDT' in info['symbol'][-4:]:
        usdt_tree.append(info['symbol'])


with open('../json/symbol_info.json', 'w') as outfile:
    json.dump(symbol_info, outfile)
with open('../json/stepsize_info.json', 'w') as outfile:
    json.dump(stepsize_info, outfile)
with open('../json/rate_limits.json', 'w') as outfile:
    json.dump(rate_limits, outfile)


with open('../json/tree/bnb_tree.json', 'w') as outfile:
    json.dump(bnb_tree, outfile)
with open('../json/tree/btc_tree.json', 'w') as outfile:
    json.dump(btc_tree, outfile)
with open('../json/tree/eth_tree.json', 'w') as outfile:
    json.dump(eth_tree, outfile)
with open('../json/tree/usdt_tree.json', 'w') as outfile:
    json.dump(usdt_tree, outfile)