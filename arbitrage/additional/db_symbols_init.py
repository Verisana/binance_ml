from info_data.models import AllRealTimeTicker
import json


def create_all_symbols():
    symbol_info = json.load(open('arbitrage/json/symbol_info.json'))
    for symbol in symbol_info:
        if 'BTC' in symbol['symbol'][-4:]:
            symbol_tree = symbol['symbol'][-3:]
        elif 'ETH' in symbol['symbol'][-4:]:
            symbol_tree = symbol['symbol'][-3:]
        elif 'BNB' in symbol['symbol'][-4:]:
            symbol_tree = symbol['symbol'][-3:]
        else:
            symbol_tree = symbol['symbol'][-4:]
        AllRealTimeTicker.objects.get_or_create(symbol=symbol['symbol'],
                                                symbol_tree=symbol_tree,
                                                )

def cross_tree_apply():
    db_symbols = AllRealTimeTicker.objects.all()
    for symbol in db_symbols:
        if symbol.symbol_tree == 'USDT':
            pair_1 = symbol.symbol[0:-4]
            for cross in db_symbols:
                if pair_1 in cross.symbol[0:-3] and cross.symbol[-4:] != 'USDT':
                    symbol.cross_symbols.add(cross)

def delete_all_entries():
    db_symbols = AllRealTimeTicker.objects.all()
    for symbol in db_symbols:
        symbol.delete()

delete_all_entries()
create_all_symbols()