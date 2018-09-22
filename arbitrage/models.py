from django.db import models
from decimal import *


class BotSettings(models.Model):
    name = models.CharField(max_length=64, unique=True)
    binance_api = models.ForeignKey('profiles.BinanceKey', on_delete=models.CASCADE)
    telegram_bot = models.ForeignKey('profiles.TelegramBotSettings', on_delete=models.CASCADE)
    stop_qty = models.IntegerField(null=True, default=0)
    profit_threshold = models.DecimalField(default=Decimal('0.5'), max_digits=6, decimal_places=3)
    switch_trading = models.BooleanField(default=False)

    def __str__(self):
        return '%s' % self.name


class OpenedDeals(models.Model):
    base_pair = models.CharField(max_length=16)
    middle_pair = models.CharField(max_length=16)
    end_pair = models.CharField(max_length=16)

    date_open = models.DateTimeField(auto_now_add=True)

    base_qty = models.DecimalField(max_digits=25, decimal_places=8)
    middle_qty = models.DecimalField(max_digits=25, decimal_places=8)
    end_qty = models.DecimalField(max_digits=25, decimal_places=8)

    base_price = models.DecimalField(max_digits=25, decimal_places=8)
    middle_price = models.DecimalField(max_digits=25, decimal_places=8)
    end_price = models.DecimalField(max_digits=25, decimal_places=8)

    base_order_id = models.CharField(max_length=32, blank=True, null=True)
    middle_order_id = models.CharField(max_length=32, blank=True, null=True)
    end_order_id = models.CharField(max_length=32, blank=True, null=True)

    is_reverse = models.BooleanField(default=False)
    is_base_order_set = models.BooleanField(default=False)
    is_middle_order_set = models.BooleanField(default=False)
    is_end_order_set = models.BooleanField(default=False)

    is_base_order_filled = models.BooleanField(default=False)
    is_middle_order_filled = models.BooleanField(default=False)
    is_end_order_filled = models.BooleanField(default=False)

    invest_amount = models.DecimalField(max_digits=10, decimal_places=2)
    expected_return = models.DecimalField(max_digits=10, decimal_places=2)
    expected_roi = models.DecimalField(max_digits=3, decimal_places=2)
    expected_profit = models.DecimalField(max_digits=10, decimal_places=2)


class ClosedDeals(models.Model):
    datetime_base_pair = models.DateTimeField(auto_now_add=True)
    datetime_middle_pair = models.DateTimeField(blank=True, null=True)
    datetime_end_pair = models.DateTimeField(blank=True, null=True)

    base_price = models.DecimalField(max_digits=25, decimal_places=8)
    middle_price = models.DecimalField(max_digits=25, decimal_places=8, blank=True, null=True)
    end_price = models.DecimalField(max_digits=25, decimal_places=8, blank=True, null=True)

    qty_to_trade = models.DecimalField(max_digits=25, decimal_places=8)

    base_pair = models.CharField(max_length=16)
    middle_pair = models.CharField(max_length=16)
    end_pair = models.CharField(max_length=16)

    invest_amount = models.DecimalField(max_digits=15, decimal_places=5)
    return_amount = models.DecimalField(max_digits=15, decimal_places=5, blank=True, null=True)
    roi = models.DecimalField(max_digits=3, decimal_places=2, blank=True, null=True)
    profit = models.DecimalField(max_digits=15, decimal_places=5, blank=True, null=True)

    expected_return = models.DecimalField(max_digits=15, decimal_places=5)
    expected_roi = models.DecimalField(max_digits=3, decimal_places=2)
    expected_profit = models.DecimalField(max_digits=15, decimal_places=5)

    reverse = models.BooleanField(default=False)

    def __str__(self):
        return 'symbols: {0} - {1} - {2}'.format(self.base_pair, self.middle_pair, self.end_pair)