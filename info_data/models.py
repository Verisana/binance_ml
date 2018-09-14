from django.db import models
from decimal import *


class AllRealTimeTicker(models.Model):
    symbol = models.CharField(max_length=16)
    updated_at = models.DateTimeField(auto_now=True)

    symbol_tree = models.CharField(max_length=64,
                                   choices=(('BTC',
                                             'BTC'),
                                            ('ETH',
                                             'ETH'),
                                            ('BNB',
                                             'BNB'),
                                            ('USDT',
                                             'USDT')
                                            ))

    best_ask_pr = models.DecimalField(max_digits=25, decimal_places=8, blank=True, null=True)
    best_ask_qty = models.DecimalField(max_digits=25, decimal_places=8, blank=True, null=True)
    best_bid_pr = models.DecimalField(max_digits=25, decimal_places=8, blank=True, null=True)
    best_bid_qty = models.DecimalField(max_digits=25, decimal_places=8, blank=True, null=True)

    pr_change = models.DecimalField(max_digits=25, decimal_places=8, blank=True, null=True)
    pr_change_per = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)

    last_pr_close = models.DecimalField(max_digits=25, decimal_places=8, blank=True, null=True)
    last_trade_qty = models.DecimalField(max_digits=25, decimal_places=8, blank=True, null=True)

    high_pr_24h = models.DecimalField(max_digits=25, decimal_places=8, blank=True, null=True)
    low_pr_24h = models.DecimalField(max_digits=25, decimal_places=8, blank=True, null=True)

    def __str__(self):
        return '%s' % self.symbol