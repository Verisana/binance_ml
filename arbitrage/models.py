from django.db import models
from decimal import *


class BotSettings(models.Model):
    name = models.CharField(max_length=64, unique=True)
    binance_api = models.ForeignKey('profiles.BinanceKey', on_delete=models.CASCADE)
    telegram_bot = models.ForeignKey('profiles.TelegramBotSettings', on_delete=models.CASCADE)
    stop_qty = models.IntegerField(null=True, default=0)
    profit_threshold = models.DecimalField(default=Decimal('0.5'), max_digits=15, decimal_places=8)
    balance = models.DecimalField(default=Decimal('0'), max_digits=15, decimal_places=8)
    switch_trading = models.BooleanField(default=False)

    def __str__(self):
        return '%s' % self.name


class Deals(models.Model):
    base_pair = models.CharField(max_length=16)
    middle_pair = models.CharField(max_length=16)
    end_pair = models.CharField(max_length=16)

    date_open = models.DateTimeField(auto_now_add=True)
    datetime_base_pair = models.DateTimeField(blank=True, null=True)
    datetime_middle_pair = models.DateTimeField(blank=True, null=True)
    datetime_end_pair = models.DateTimeField(blank=True, null=True)

    init_qty = models.DecimalField(max_digits=25, decimal_places=8)
    transit_qty = models.DecimalField(max_digits=25, decimal_places=8, blank=True, null=True)

    base_price = models.DecimalField(max_digits=25, decimal_places=8, blank=True, null=True)
    middle_price = models.DecimalField(max_digits=25, decimal_places=8, blank=True, null=True)
    end_price = models.DecimalField(max_digits=25, decimal_places=8, blank=True, null=True)
    expected_base_price = models.DecimalField(max_digits=25, decimal_places=8)
    expected_middle_price = models.DecimalField(max_digits=25, decimal_places=8)
    expected_end_price = models.DecimalField(max_digits=25, decimal_places=8)

    base_order_id = models.CharField(max_length=32, blank=True, null=True)
    middle_order_id = models.CharField(max_length=32, blank=True, null=True)
    end_order_id = models.CharField(max_length=32, blank=True, null=True)

    reverse = models.BooleanField(default=False)
    is_traded = models.BooleanField(default=False)

    expected_invest = models.DecimalField(max_digits=25, decimal_places=8)
    invest = models.DecimalField(max_digits=25, decimal_places=8, blank=True, null=True)

    return_amount = models.DecimalField(max_digits=25, decimal_places=8, blank=True, null=True)
    roi = models.DecimalField(max_digits=3, decimal_places=2, blank=True, null=True)
    profit = models.DecimalField(max_digits=25, decimal_places=8, blank=True, null=True)

    expected_return = models.DecimalField(max_digits=25, decimal_places=8)
    expected_roi = models.DecimalField(max_digits=3, decimal_places=2)
    expected_profit = models.DecimalField(max_digits=25, decimal_places=8)

    hypothetical_invest = models.DecimalField(max_digits=25, decimal_places=8)
    hypothetical_return = models.DecimalField(max_digits=25, decimal_places=8)
    hypothetical_profit = models.DecimalField(max_digits=25, decimal_places=8)

    def __str__(self):
        return '{0} - {1} - {2}'.format(self.base_pair, self.middle_pair, self.end_pair)