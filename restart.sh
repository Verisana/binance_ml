systemctl restart nginx
systemctl restart uwsgi
pkill -f /home/leo/binance_ml/manage.py connect_binance
nohup python3 /home/leo/binance_ml/manage.py connect_binance --type=all_ticker &