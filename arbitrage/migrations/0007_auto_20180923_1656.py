# Generated by Django 2.1.1 on 2018-09-23 11:56

from decimal import Decimal
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('arbitrage', '0006_auto_20180922_1557'),
    ]

    operations = [
        migrations.CreateModel(
            name='Deals',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('base_pair', models.CharField(max_length=16)),
                ('middle_pair', models.CharField(max_length=16)),
                ('end_pair', models.CharField(max_length=16)),
                ('date_open', models.DateTimeField(auto_now_add=True)),
                ('datetime_base_pair', models.DateTimeField(blank=True, null=True)),
                ('datetime_middle_pair', models.DateTimeField(blank=True, null=True)),
                ('datetime_end_pair', models.DateTimeField(blank=True, null=True)),
                ('base_qty', models.DecimalField(decimal_places=8, max_digits=25)),
                ('middle_qty', models.DecimalField(blank=True, decimal_places=8, max_digits=25, null=True)),
                ('end_qty', models.DecimalField(blank=True, decimal_places=8, max_digits=25, null=True)),
                ('base_price', models.DecimalField(decimal_places=8, max_digits=25)),
                ('expected_middle_price', models.DecimalField(decimal_places=8, max_digits=25)),
                ('expected_end_price', models.DecimalField(decimal_places=8, max_digits=25)),
                ('real_middle_price', models.DecimalField(blank=True, decimal_places=8, max_digits=25, null=True)),
                ('real_end_price', models.DecimalField(blank=True, decimal_places=8, max_digits=25, null=True)),
                ('base_order_id', models.CharField(blank=True, max_length=32, null=True)),
                ('middle_order_id', models.CharField(blank=True, max_length=32, null=True)),
                ('end_order_id', models.CharField(blank=True, max_length=32, null=True)),
                ('reverse', models.BooleanField(default=False)),
                ('is_successful', models.BooleanField(default=False)),
                ('invest_amount', models.DecimalField(decimal_places=8, max_digits=25)),
                ('return_amount', models.DecimalField(blank=True, decimal_places=5, max_digits=15, null=True)),
                ('roi', models.DecimalField(blank=True, decimal_places=2, max_digits=3, null=True)),
                ('profit', models.DecimalField(blank=True, decimal_places=5, max_digits=15, null=True)),
                ('expected_return', models.DecimalField(decimal_places=8, max_digits=25)),
                ('expected_roi', models.DecimalField(decimal_places=2, max_digits=3)),
                ('expected_profit', models.DecimalField(decimal_places=8, max_digits=25)),
                ('hypothetical_invest', models.DecimalField(decimal_places=8, max_digits=25)),
                ('hypothetical_return', models.DecimalField(decimal_places=8, max_digits=25)),
                ('hypothetical_profit', models.DecimalField(decimal_places=8, max_digits=25)),
            ],
        ),
        migrations.DeleteModel(
            name='ClosedDeals',
        ),
        migrations.DeleteModel(
            name='OpenedDeals',
        ),
        migrations.AddField(
            model_name='botsettings',
            name='balance',
            field=models.DecimalField(decimal_places=8, default=Decimal('0'), max_digits=15),
        ),
        migrations.AlterField(
            model_name='botsettings',
            name='profit_threshold',
            field=models.DecimalField(decimal_places=8, default=Decimal('0.5'), max_digits=15),
        ),
    ]
