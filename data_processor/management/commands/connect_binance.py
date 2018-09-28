import json
from decimal import *
from binance.websockets import BinanceSocketManager
from binance.client import Client
from arbitrage.models import BotSettings
from django.core.management.base import BaseCommand
from info_data.models import AllRealTimeTicker
from arbitrage.algo_bot import ExecutePriceTunnel, PriceTunnelTrader


class Command(BaseCommand):
    help = 'Open websocket connection to binance'

    bot = BotSettings.objects.all()[0]
    client = Client(bot.binance_api.api_key, bot.binance_api.api_secret)
    bm = BinanceSocketManager(client)

    def add_arguments(self, parser):
        parser.add_argument(
            '--type', action='store', required=True,
            help='Type connection',
        )
        parser.add_argument(
            '--symbol', action='store',
            help='Specific symbol',
        )

    def handle(self, *args, **options):
        if options['type'] == 'all_ticker':
            all_ticker = self.bm.start_ticker_socket(self.process_all_ticker_message)
        elif options['type'] == 'user_info':
            user = self.bm.start_user_socket(self.processs_user_message)
        elif options['type'] == 'ticker' and options['symbol']:
            ticker = self.bm.start_symbol_ticker_socket(options['symbol'], self.process_ticker_message)
        self.bm.start()

    def process_all_ticker_message(self, msgs):
        for msg in msgs:
            try:
                symbol = AllRealTimeTicker.objects.get(symbol=msg['s'])
            except:
                exec(open('arbitrage/additional/symbols_dump.py').read())
                exec(open('arbitrage/additional/tree_cross_forming.py').read())
                exec(open('arbitrage/additional/db_symbols_init.py').read())
                continue

            symbol.best_ask_pr = Decimal(msg['a'])
            symbol.best_ask_qty = Decimal(msg['A'])
            symbol.best_bid_pr = Decimal(msg['b'])
            symbol.best_bid_qty = Decimal(msg['B'])
            symbol.pr_change = Decimal(msg['p'])
            symbol.pr_change_per = Decimal(msg['P'])
            symbol.last_pr_close = Decimal(msg['c'])
            symbol.last_trade_qty = Decimal(msg['Q'])
            symbol.high_pr_24h = Decimal(msg['h'])
            symbol.low_pr_24h = Decimal(msg['l'])
            symbol.save()
        self.usdt_tunnel_executor()

    def usdt_tunnel_executor(self):
        ept = ExecutePriceTunnel()
        tunnels = ept.check_usdt_simple()
        trader = PriceTunnelTrader(tunnels)
        trader.check_profit_trade()

    def processs_user_message(self, msg):
        print(msg)
        if msg['e'] == 'outboundAccountInfo':
            for balance in msg['B']:
                if balance['a'] == 'USDT':
                    self.bot.balance = Decimal(balance['f'])
                    self.bot.save()
                    break

    def process_ticker_message(self, msg):
        print(msg)