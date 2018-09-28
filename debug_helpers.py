from profiles.models import BinanceKey
from binance.client import Client
from binance.websockets import BinanceSocketManager
from info_data.models import AllRealTimeTicker
from profiles.models import TelegramBotSettings
import telegram
from arbitrage.models import Deals
import json
from decimal import *
from arbitrage.algo_bot import ExecutePriceTunnel, PriceTunnelTrader


def process_m_message(msg):
    print("stream: {} data: {}".format(msg['stream'], msg['data']))

def process_message(msg):
    print(msg)

bk = BinanceKey.objects.get(name='binance_test')
client = Client(bk.api_key, bk.api_secret)
bm = BinanceSocketManager(client)
ticker = bm.start_ticker_socket(process_message)
diff_key = bm.start_depth_socket('BNBBTC', process_message)
#bm.start()
#bm.start_user_socket(process_message)

#exec(open('arbitrage/algo_bot.py').read())
#exec(open('arbitrage/additional/symbols_dump.py').read())
#exec(open('arbitrage/additional/tree_cross_forming.py').read())
#exec(open('arbitrage/additional/db_symbols_init.py').read())

ept = ExecutePriceTunnel()
res = ept.check_usdt_simple()
all = AllRealTimeTicker.objects.all()
symbol_info_key = json.load(open('arbitrage/json/symbol_info_key.json'))
symbol_info_list = json.load(open('arbitrage/json/symbol_info_list.json'))

tel_bot_set = TelegramBotSettings.objects.all()
pp = telegram.utils.request.Request(proxy_url='https://10.0.2.2:1080')
telegram_bot = telegram.Bot(token=tel_bot_set[0].token, request=pp)
message = 'Test'
chat_id = tel_bot_set[0].chat.all()
telegram_bot.send_message(chat_id[0].chat_id, message)

#celery flower -A binance_ml --loglevel=INFO
#celery -A binance_ml worker -l info --purge


'''
nohup /home/leo/Env/binance_ml/bin/python3 /home/leo/binance_ml/manage.py connect_binance --type=all_ticker &
nohup /home/leo/Env/binance_ml/bin/python3 /home/leo/binance_ml/manage.py connect_binance --type=user_info &
ps -aux | grep manage.py
pkill -f /home/leo/binance_ml/manage.py
'''
#{'symbol': 'ADAUSDT', 'orderId': 26551136, 'clientOrderId': 'zdowRoY9a8cuudfxgQYtmb', 'transactTime': 1537812610251, 'price': '0.08685000', 'origQty': '120.00000000', 'executedQty': '120.00000000', 'cummulativeQuoteQty': '10.42200000', 'status': 'FILLED', 'timeInForce': 'IOC', 'type': 'LIMIT', 'side': 'BUY', 'fills': [{'price': '0.08685000', 'qty': '120.00000000', 'commission': '0.12000000', 'commissionAsset': 'ADA', 'tradeId': 6716086}]}
#{'symbol': 'ADAUSDT', 'orderId': 26551303, 'clientOrderId': 'BNwY1JCWj8EYtYY5LLpLEi', 'transactTime': 1537812702694, 'price': '0.08686000', 'origQty': '120.00000000', 'executedQty': '120.00000000', 'cummulativeQuoteQty': '10.42440000', 'status': 'FILLED', 'timeInForce': 'IOC', 'type': 'LIMIT', 'side': 'SELL', 'fills': [{'price': '0.08687000', 'qty': '120.00000000', 'commission': '0.01042440', 'commissionAsset': 'USDT', 'tradeId': 6716138}]}

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