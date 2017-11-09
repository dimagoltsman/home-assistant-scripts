import requests, json
import sqlite3

def get_pass():
    pass_f = open("/home/homeassistant/.homeassistant/scripts/pass", 'r')
    PASS = pass_f.read()
    pass_f.close()
    return PASS


def split_array(arr, size):
    arrs = []
    while len(arr) > size:
        pice = arr[:size]
        arrs.append(pice)
        arr   = arr[size:]
    arrs.append(arr)
    return arrs

def getApi(entity):
    headers = {'content-type': 'application/json', 'x-ha-access': get_pass()}
    r = requests.get("http://127.0.0.1:8123/api/" + entity, headers=headers)
    return r.json()

def execute_hass_sql(query):
    conn = sqlite3.connect('/home/homeassistant/.homeassistant/home-assistant_v2.db')
    c = conn.cursor()
    res = c.execute(query).fetchall()
    c.close()
    return res
