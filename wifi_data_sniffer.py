from scapy.all import *
import pandas as pd
import subprocess as sub
import time
import os
import sys

#Loading the data generated from wifi_scanner
df = pd.read_csv("networks.csv", sep='\t')

#For every wifi scanned from wifi_scanner find all the DATA packets and losted packets
for index, row in df.iterrows():
    p = sub.Popen(['airodump-ng','--bssid', row["BSSID"], '--essid', row["SSID"], '-c', str(row["Channel"]), '-w', "network", '--output-format', 'csv', 'wlan0mon'])
    time.sleep(10)
    p.kill()