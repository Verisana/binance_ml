# Generated by Django 2.1.1 on 2018-09-20 18:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('arbitrage', '0002_auto_20180919_1354'),
    ]

    operations = [
        migrations.RenameField(
            model_name='closeddeals',
            old_name='base_qty',
            new_name='qty_to_trade',
        ),
        migrations.RemoveField(
            model_name='closeddeals',
            name='end_qty',
        ),
        migrations.RemoveField(
            model_name='closeddeals',
            name='middle_qty',
        ),
        migrations.AddField(
            model_name='openeddeals',
            name='is_reverse',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='botsettings',
            name='stop_qty',
            field=models.IntegerField(default=0, null=True),
        ),
    ]
