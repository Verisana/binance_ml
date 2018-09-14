from profiles.models import BinanceKey
from binance.client import Client
from binance.websockets import BinanceSocketManager
from info_data.models import AllRealTimeTicker
from profiles.models import TelegramBotSettings
import telegram


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

from arbitrage.algo_bot import BinancePriceTunnel, ExecutePriceTunnel
ept = ExecutePriceTunnel()
res = ept.check_usdt_simple()
usdt_tunnel_executor()
all = AllRealTimeTicker.objects.all()

tel_bot_set = TelegramBotSettings.objects.all()
pp = telegram.utils.request.Request(proxy_url='https://10.0.2.2:1080')
telegram_bot = telegram.Bot(token=tel_bot_set[0].token, request=pp)
message = 'Test'
chat_id = tel_bot_set[0].chat.all()
telegram_bot.send_message(chat_id[0].chat_id, message)

#celery flower -A binance_ml --loglevel=INFO
#celery -A binance_ml worker -l info --purge
pp = telegram.utils.request.Request(proxy_url='https://10.0.2.2:1080')