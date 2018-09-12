from profiles.models import BinanceKey
from binance.client import Client
from binance.websockets import BinanceSocketManager


def process_m_message(msg):
    print("stream: {} data: {}".format(msg['stream'], msg['data']))

def process_message(msg):
    print(msg)

bk = BinanceKey.objects.get(name='binance_test')
client = Client(bk.api_key, bk.api_secret)
bm = BinanceSocketManager(client)
ticker = bm.start_ticker_socket(process_message)
diff_key = bm.start_depth_socket('BNBBTC', process_message)
bm.start()
#conn_key = bm.start_multiplex_socket(['bnbbtc@aggTrade'], process_m_message)
bm.start_user_socket(process_message)

exec(open('arbitrage/main.py').read())
