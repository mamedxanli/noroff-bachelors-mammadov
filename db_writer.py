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

def build_influx_tcp_structure(measurement: str, epoch: str, tags: dict = {}, fields: dict = {}) -> dict:
    """
    Builds data structure for Influx. To be used in the TCP port localhost:8086.\n
    This port is the InfluxDB Docker container running.
    If no epoch is passed, defaults to datetime.now().\n
    Expects:\n
        - measurement: Main value to search in Grafana. (similar to Table name)
        - value: The value of said measurement. Defaults to float 1. Unless the measurement is really simple with no relation to "fields", leave it at default.
        - epoch: Timestamp of the measurement. Format is 2019-03-20T00:08:44
        - fields: Optional: Dict if more fields want to be stored. Fields can contain values, like cpu usage, temperature, or traffic. Usually used with numeric values for plot.
        - tags: Optional: Dict with tags for this measurement. Tags can be used as identifiers or labels. Usually strings to sort data by groups.
    """
    try:
        
        # value goes into fields, more like a placeholder
        fields["value"] = float(value)
        # Main dictionary
        data = {
            "measurement" : measurement,
            "epoch"       : epoch
            }
        # Nest dictionaries
        data["tags"] = tags
        tags = {
            "country"
            "continent"
        }
        data["fields"] = fields
        fields = {
            "epoch" : epoch,
            "ip" : ip,
            "geohash_data" : geohash_data,
            "latitude" : latitude,
            "latitude" : latitude,
        }
        print(data) # Debug
        return data
    except Exception as exc:
        raise ValueError(f"Exception while building influx tcp structure: {exc}.")

input_data = process_input_data(logfile)
build_influx_tcp_structure('ssh_honeypot', input_data)

#print(data)

