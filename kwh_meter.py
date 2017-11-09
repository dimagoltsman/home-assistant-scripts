#!/usr/bin/env python3

import importlib.util
spec = importlib.util.spec_from_file_location("utils", "/home/homeassistant/.homeassistant/scripts/utils.py")
Utils = importlib.util.module_from_spec(spec)
spec.loader.exec_module(Utils)

from datetime import datetime, timedelta
import requests, json

KW_MULTIPLYER = 0.001
MINUTES_IN_HOUR = 60

def get_input_date(id):
    date = Utils.getApi('states/input_datetime.' + id)
    attr = date['attributes']
    dt = datetime(attr['year'], attr['month'], attr['day'])
    return dt

from_d = get_input_date('kwh_from').strftime('%Y-%m-%d %H:%M:%S')
to_d =   get_input_date('kwh_to').strftime('%Y-%m-%d %H:%M:%S')

query = """
select CAST(state as DECIMAL) as kw, last_updated as time from states where entity_id = 'sensor.last_minute_avarage'
and last_updated between date('"""   + from_d + """') and date('""" + to_d + """') order by time asc
"""
res = Utils.execute_hass_sql(query)


res = list(map(lambda x: x[0], res))
splitted = Utils.split_array(res, MINUTES_IN_HOUR)
sums = list(map(lambda a: (sum(a) / MINUTES_IN_HOUR) * KW_MULTIPLYER , splitted))
total = sum(sums)


print(str("{:.3f}".format(total)))

