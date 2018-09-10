from profiles.models import BinanceKey
from binance.client import Client


bk = BinanceKey.objects.get(name='binance_test')
client = Client(bk.api_key, bk.api_secret)

exec(open('arbitrage/main.py').read())
