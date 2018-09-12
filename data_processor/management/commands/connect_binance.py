from binance.websockets import BinanceSocketManager
from binance.client import Client
from profiles.models import BinanceKey
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = 'Open websocket connection to binance'

    bk = BinanceKey.objects.get(name='binance_test')
    client = Client(bk.api_key, bk.api_secret)
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
            ticker = self.bm.start_ticker_socket(self.process_ticker_message)
            self.bm.start()
        elif options['type'] == 'user_info':
            user = self.bm.start_user_socket(self.processs_user_message)
            self.bm.start()

    def process_ticker_message(self, msgs):
        for msg in msgs:
            print("message type: {}".format(msg['e']))
            print(msg)

    def processs_user_message(self, msg):
        print(msg)