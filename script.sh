#!/bin/sh
PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/home/apipilikas/Desktop/adke
python3 wifi_scanner.py wlan0mon
python3 wifi_data_sniffer.py
python3 evaluator.py
rm *.csv