# -*- coding: utf-8 -*-
"""
Created on Tue Jul 25 16:56:39 2023

@author: sfelc
"""

import pandas as pd
import requests
from apscheduler.schedulers.blocking import BlockingScheduler
import datetime

# @sched.scheduled_job('interval', seconds=20)
def scrape_stations():
    url = "https://wroclawskirower.pl/mapa-stacji/"
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    result = requests.get(url, headers=headers)
    html = (result.content.decode())
    data = pd.read_html(html)
    data = data[0].drop(['Nazwa stacji', 'Współrzędne', 'Liczba stojaków'], axis = 1)
    timestamp = datetime.datetime.now()
    stringstamp = timestamp.strftime("%m-%d-%Y %H:%M:%S")
    data['time'] = stringstamp
    f = open("metadata.txt","r")
    n = int(f.readline())
    n2 = int(f.readline())
    f.close()
    namestring = "Stacje/data"+str(n)+".csv" # change path and filename here
    data.to_csv(namestring)    
    f = open("metadata.txt","w")
    n += 1
    f.write(str(n)+"\n")
    f.write(str(n2))
    f.close()

scheduler = BlockingScheduler()
scheduler.add_job(scrape_stations, 'interval', minutes=5)
scheduler.start()