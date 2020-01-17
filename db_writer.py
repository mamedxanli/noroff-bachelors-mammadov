import time
from datetime import datetime
from influxdb import client as influxdb
import re
import sys
import json
import geoip
from contextlib import suppress
import geohash

logfile = '/var/log/auth.log'
dbname = 'honeypot'
measurement = 'ssh_honeypot'


def get_geolocation(ip):
    data = geoip.geolite2.lookup(ip)
    return data.to_dict()


def process_input_data(logfile):
    regex_value = r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}'
    #reads logfile, parses it and returns epoch, ip, continent, country, location and geohash
    with open(logfile, 'r') as f:
        for line in f:
            #with suppress(Exception):
                try:
                    ip = str((re.findall(regex_value, line)))
                    epoch = line[0:26]
                    geodata = get_geolocation(ip[2:-2])
                    continent = geodata['continent']
                    country = geodata['country']
                    location = geodata['location']
                    latlong = [x.strip() for x in str(location).split(',')]
                    latitude = latlong[0]
                    longitude = latlong[1]
                    geohash_data = geohash.encode(float(latitude[1:]), float(longitude[:0-1]))
                    #print(epoch, ip, continent, country, location, geohash_data)
                    return epoch, ip, continent, country, location, geohash_data
                except Exception as exc:
                    raise ValueError(f"Exception while getting geodata: {exc}.")
data = process_input_data(logfile)
print(data)
