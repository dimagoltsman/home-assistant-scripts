#!/usr/bin/env python3

import json
import importlib.util
spec = importlib.util.spec_from_file_location("utils", "/home/homeassistant/.homeassistant/scripts/utils.py")
Utils = importlib.util.module_from_spec(spec)
spec.loader.exec_module(Utils)

from datetime import datetime, timedelta
import requests, json

delete_events = "DELETE FROM hass.events WHERE time_fired < DATE_SUB( NOW() , INTERVAL 8 DAY );"

delete_states = """
delete FROM hass.states where 
entity_id in ("sensor.voltage", "sensor.current", "sensor.power", "sensor.ram_available", "sensor.cpu_used", "sensor.price", 'sensor.ram_free', 'sensor.cpu_temperature') 
and last_updated < DATE_SUB( NOW() , INTERVAL 8 DAY );
""" 
optimize_states = "OPTIMIZE TABLE hass.states;"
optimize_events = "OPTIMIZE TABLE hass.events;"

Utils.execute_hass_mysql(delete_events)
Utils.execute_hass_mysql(delete_states)
Utils.execute_hass_mysql(optimize_states)
Utils.execute_hass_mysql(optimize_events)
