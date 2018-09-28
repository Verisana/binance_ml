import json


symbol_info_list = json.load(open('arbitrage/json/symbol_info_list.json'))
symbol_info_key = json.load(open('arbitrage/json/symbol_info_key.json'))
usdt_array = json.load(open('arbitrage/json/tree/usdt_tree.json'))
btc_array = json.load(open('arbitrage/json/tree/btc_tree.json'))
eth_array = json.load(open('arbitrage/json/tree/eth_tree.json'))
bnb_array = json.load(open('arbitrage/json/tree/bnb_tree.json'))

btc_eth_cross = []
btc_bnb_cross = []
btc_usdt_cross = []
eth_bnb_cross = []
eth_usdt_cross = []
bnb_usdt_cross = []
btc_eth_bnb_cross = []
btc_eth_usdt_cross = []
btc_bnb_usdt_cross = []
eth_bnb_usdt_cross = []
btc_eth_bnb_usdt_cross = []

for i in btc_array:
    for k in eth_array:
        if i[:-3] == k[:-3]:
            btc_eth_cross.append(i[:-3])
    for k in bnb_array:
        if i[:-3] == k[:-3]:
            btc_bnb_cross.append(i[:-3])
    for k in usdt_array:
        if i[:-3] == k[:-4]:
            btc_usdt_cross.append(i[:-3])

for i in eth_array:
    for k in bnb_array:
        if i[:-3] == k[:-3]:
            eth_bnb_cross.append(i[:-3])
    for k in usdt_array:
        if i[:-3] == k[:-4]:
            eth_usdt_cross.append(i[:-3])

for i in bnb_array:
    for k in usdt_array:
        if i[:-3] == k[:-4]:
            bnb_usdt_cross.append(i[:-3])

for i in btc_eth_cross:
    for k in bnb_array:
        if i == k[:-3]:
            btc_eth_bnb_cross.append(i)
    for k in usdt_array:
        if i == k[:-4]:
            btc_eth_usdt_cross.append(i)

for i in btc_bnb_cross:
    for k in usdt_array:
        if i == k[:-4]:
            btc_bnb_usdt_cross.append(i)

for i in eth_bnb_cross:
    for k in usdt_array:
        if i == k[:-4]:
            eth_bnb_usdt_cross.append(i)

for i in btc_eth_bnb_cross:
    for k in usdt_array:
        if i == k[:-4]:
            btc_eth_bnb_usdt_cross.append(i)


with open('arbitrage/json/cross/btc_eth_cross.json', 'w') as outfile:
    json.dump(btc_eth_cross, outfile)
with open('arbitrage/json/cross/btc_bnb_cross.json', 'w') as outfile:
    json.dump(btc_bnb_cross, outfile)
with open('arbitrage/json/cross/btc_usdt_cross.json', 'w') as outfile:
    json.dump(btc_usdt_cross, outfile)
with open('arbitrage/json/cross/eth_bnb_cross.json', 'w') as outfile:
    json.dump(eth_bnb_cross, outfile)
with open('arbitrage/json/cross/eth_usdt_cross.json', 'w') as outfile:
    json.dump(eth_usdt_cross, outfile)
with open('arbitrage/json/cross/bnb_usdt_cross.json', 'w') as outfile:
    json.dump(bnb_usdt_cross, outfile)
with open('arbitrage/json/cross/btc_eth_bnb_cross.json', 'w') as outfile:
    json.dump(btc_eth_bnb_cross, outfile)
with open('arbitrage/json/cross/btc_eth_usdt_cross.json', 'w') as outfile:
    json.dump(btc_eth_usdt_cross, outfile)
with open('arbitrage/json/cross/btc_bnb_usdt_cross.json', 'w') as outfile:
    json.dump(btc_bnb_usdt_cross, outfile)
with open('arbitrage/json/cross/eth_bnb_usdt_cross.json', 'w') as outfile:
    json.dump(eth_bnb_usdt_cross, outfile)
with open('arbitrage/json/cross/btc_eth_bnb_usdt_cross.json', 'w') as outfile:
    json.dump(btc_eth_bnb_usdt_cross, outfile)
