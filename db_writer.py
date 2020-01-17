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
    regex_pattern = r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}'
    regex_value = re.compile(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}')
    all_lines_processed = list()
    with open(logfile, 'r') as f:
        #while True:
            for line in f:
                if re.findall(regex_pattern, line) == []:
                    continue
                else:
                    output = {}
                    ip = str(re.findall(regex_pattern, line))[2:-2]
                    geodata = get_geolocation(ip)
                    epoch = line[0:26]
                    continent = geodata['continent']
                    country = geodata['country']
                    location = geodata['location']
                    latlong = [x.strip() for x in str(location).split(',')]
                    latitude = latlong[0]
                    longitude = latlong[1]
                    geohash_data = geohash.encode(float(latitude[1:]), float(longitude[:0-1]))
                    output["ip"] = ip
                    output["epoch"] = epoch
                    output["continent"] = continent
                    output["country"] = country
                    output["latitude"] = latitude[1:]
                    output["longitude"] = longitude[:-1]
                    output["geohash_data"] = geohash_data
                all_lines_processed.append(output)
            return all_lines_processed

data = process_input_data(logfile)
print(data)

