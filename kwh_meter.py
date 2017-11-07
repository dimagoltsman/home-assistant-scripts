#!/usr/bin/env python3

import sqlite3
from datetime import datetime, timedelta
import requests, json

KW_MULTIPLYER = 0.001
MINUTES_IN_HOUR = 60.0

def get_pass():
  pass_f = open("/home/homeassistant/.homeassistant/scripts/pass", 'r')
  PASS = pass_f.read()
  pass_f.close()
  return PASS
  
def getApi(url):
    headers = {'content-type': 'application/json', 'x-ha-access': get_pass()}
    r = requests.get(url, headers=headers)
    return r.json()
    
def get_input_date(id):
    date = getApi('http://127.0.0.1:8123/api/states/input_datetime.' + id)
    attr = date['attributes']
    dt = datetime(attr['year'], attr['month'], attr['day'])
    return dt
    
def get_from_date():    
    return get_input_date('kwh_from')
    
def get_to_date():    
    return get_input_date('kwh_to')

def split(arr, size):
     arrs = []
     while len(arr) > size:
         pice = arr[:size]
         arrs.append(pice)
         arr   = arr[size:]
     arrs.append(arr)
     return arrs

conn = sqlite3.connect('/home/homeassistant/.homeassistant/home-assistant_v2.db')
c = conn.cursor()
from_d = get_from_date().strftime('%Y-%m-%d %H:%M:%S')
to_d = get_to_date().strftime('%Y-%m-%d %H:%M:%S')

res = c.execute("""
select CAST(state as DECIMAL) as kw, last_updated as time from states where entity_id = 'sensor.last_minute_avarage'
and last_updated between date('""" + from_d+ """') and date('""" + to_d + """') order by time asc
""").fetchall()

res = list(map(lambda x: x[0], res))
splitted = split(res, 60)
sums = list(map(lambda a: (sum(a) / MINUTES_IN_HOUR) * KW_MULTIPLYER , splitted))
total = sum(sums)
c.close()

print(str("{:.3f}".format(total)))


